SELECT {p:code}         AS product_code,
       {p:name[de]}     AS product_name,
       {pr:price}       AS product_price,
       {p:creationTime} AS product_creation_time,
       {cat:code}       AS category_source
FROM {
    Product AS p
    JOIN CategoryProductRelation AS cpr ON {cpr.target}={p.pk}
    JOIN Category AS cat ON {cat.pk}={cpr.source}
    JOIN ArticleApprovalStatus as st on {p.approvalstatus}={st.pk}
    JOIN CatalogVersion AS cv ON {p.catalogVersion}={cv.pk}
    JOIN PriceRow AS pr ON {pr.product}={p.pk}}
WHERE {st.code}='approved' AND {cv:version}='Online'
ORDER BY {p:code} ASC