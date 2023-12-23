import io

import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient

import api.core.services.collection.evidence as service_evidence
import api.core.services.collection.user as service_user
import api.core.services.collection.item as service_item
from fastapi.responses import StreamingResponse
import pandas as pd


async def get_click_behavior(conn: AsyncIOMotorClient):
    # Get all evidence from DB
    evidence = await service_evidence.get_all_evidence(conn)

    # Filter only relevant events
    events = ['view', 'click']
    evidence = [e for e in evidence if e['name'] in events]

    # Filter only PDP paths
    evidence = [e for e in evidence if '/p/' in e['path']]

    # df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    df = pd.DataFrame(evidence)

    # Create columns
    df['duration'] = (df.data.apply(lambda d: d['duration']).astype('float32') / 1000).astype('int32')
    df['reco_items'] = df.data.apply(lambda d: [int(i) for i in d['items']] if 'items' in d.keys() else "")
    df['click_item'] = df.data.apply(lambda d: d['item'] if 'item' in d.keys() else 0).astype('int16')
    df['focal_item'] = df.path.apply(lambda p: convert_path_to_item_id(p))
    df['is_mobile'] = df.device_info.apply(lambda d: d['is_mobile'])

    # Convert mobile
    devices = [[False, False, False], [True, True, True]]
    df = df[df['is_mobile'].isin(devices)]
    df['is_mobile'] = df['is_mobile'].apply(lambda m: 0 if sum(m) == 0 else 1)

    # Delete columns
    df = df.drop(columns=['_id', 'device_info', 'path', 'data'])

    ## Merge User Info ##
    user = await service_user.get_all_user(conn)
    df_user = pd.DataFrame(user)[['_id', 'groups']]
    df_user['_id'] = df_user['_id'].apply(lambda id: str(id))
    df = df.merge(df_user, how='left', left_on='user_uid', right_on='_id')
    df['group'] = df.groups.apply(lambda g: g['split1'])
    df = df.drop(columns=['_id', 'groups'])

    # The click event does not track the recommended items
    # -> TODO: new version of reco2js needs to track recommendations
    df = df.sort_values(['user_uid', 'timestamp'])
    df = df.reset_index(drop=True)
    df['reco_items2'] = df['reco_items'].shift(1)
    df.loc[df['reco_items'] == '', 'reco_items'] = df['reco_items2']
    df = df.drop(columns=['reco_items2'])

    # Remove double clicks
    df = df[df['reco_items'] != '']

    # Remove rows with missing recommended items
    # df = df[df['reco_items'].str.len() != 0]

    # Since you can not group a list you need to convert to string
    df['reco_items'] = [','.join(map(str, l)) for l in df['reco_items']]

    # Aggregate user click behavior
    x = df.groupby(['user_uid', 'group', 'is_mobile', 'focal_item', 'reco_items'])['click_item'].idxmax()
    y = df.loc[x]
    df = y.sort_values(['user_uid', 'timestamp']).reset_index(drop=False)
    df = df[['user_uid', 'group', 'is_mobile', 'timestamp', 'focal_item', 'reco_items', 'click_item']]
    # df = pd.DataFrame(
    #     df.groupby(['user_uid', 'group', 'is_mobile', 'focal_item', 'reco_items'])[
    #         'click_item'].max()).reset_index()

    # Get a click yes/no column
    df['click'] = (df['click_item'] > 0).astype('int8')

    # Calculate a click position column
    df['click_pos'] = 0
    df['reco_items_h'] = df['reco_items'].apply(
        lambda i: [int(a) for a in i.split(',') if len(a) > 0])  # create list of ints
    for index, row in df[['click_item', 'reco_items_h']].iterrows():
        try:
            df.loc[index, 'click_pos'] = row['reco_items_h'].index(row['click_item']) + 1
        except:
            pass
    df = df.drop(columns=['reco_items_h'])

    # Create column for each recommended item
    N_RECOS = 3
    df['reco_items'] = df['reco_items'].apply(lambda i: [int(a) for a in i.split(',') if len(a) > 0])
    for i in range(N_RECOS):
        df[f'reco_item{i + 1}'] = df.reco_items.apply(lambda r: r[i] if len(r)>0 else 0)
    df = df.drop(columns=['reco_items'])

    ## Merge Item Info ##
    item = await service_item.get_all_items(conn)
    df_item = pd.DataFrame(item)[['id', 'created_time', 'price']]
    df_item['id'] = df_item['id'].astype('int16')
    df['focal_item_price'] = df.merge(df_item, how='left', left_on='focal_item', right_on='id')['price']
    df['reco_item1_price'] = df.merge(df_item, how='left', left_on='reco_item1', right_on='id')['price']
    df['reco_item2_price'] = df.merge(df_item, how='left', left_on='reco_item2', right_on='id')['price']
    df['reco_item3_price'] = df.merge(df_item, how='left', left_on='reco_item3', right_on='id')['price']

    stream = io.StringIO()
    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=click_behavior.csv"

    return response


def convert_path_to_item_id(s):
    """Converts the path URL into the base item ID."""
    try:
        s = s[s.find('/p/') + 3:s.find('/p/') + 21]
        s = int(s)
        if s > 9999:
            return int(str(s)[:-3])
        else:
            return s
    except:
        return s
