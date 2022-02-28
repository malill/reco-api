SELECT {o:code}         AS order_code,
       {p:code}         AS product_code,
       {oe:quantity}    AS quantity,
       {oe:basePrice}   AS product_price,
       {oe:totalPrice}  AS order_entry_total_price,
       {o:deliveryCost} as order_delivery_cost,
       {o:totalPrice}   AS order_total_price,
       {u:uid}          AS user_uid,
       {o:date}         AS order_date
FROM {
Order AS o
    JOIN OrderEntry AS oe
ON {o.pk} = {oe.order}
    JOIN Product AS p ON {p.pk} = {oe.product}
    JOIN User AS u ON {u.pk} = {o.user}}
ORDER BY {o:code} DESC