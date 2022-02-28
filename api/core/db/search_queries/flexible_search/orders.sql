SELECT {o:code}         AS order_code,
       {o:deliveryCost} as order_delivery_cost,
       {o:totalPrice}   AS order_total_price,
       {u:uid}          AS user_uid,
       {o:date}         AS order_date
FROM {
Order AS o
    JOIN User AS u
ON {u.pk} = {o.user}}
ORDER BY {o:code} DESC