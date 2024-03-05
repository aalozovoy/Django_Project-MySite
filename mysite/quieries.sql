select "shopapp_product"."id",
"shopapp_product"."name",
"shopapp_product"."description",
"shopapp_product"."price",
"shopapp_product"."discount",
"shopapp_product"."crested_at",
"shopapp_product"."archived",
"shopapp_product"."created_by_id",
"shopapp_product"."preview" from "shopapp_product" where not
"shopapp_product"."archived" order by
"shopapp_product"."price" asc,
"shopapp_product"."name" asc; args=(); alias=default


SELECT "shopapp_product"."id",
"shopapp_product"."name",
"shopapp_product"."description",
"shopapp_product"."price",
"shopapp_product"."discount",
"shopapp_product"."crested_at",
"shopapp_product"."archived",
"shopapp_product"."created_by_id",
"shopapp_product"."preview" FROM "shopapp_product" WHERE "shopapp_product"."id" = 2 LIMIT 21; args=(2,); alias=default
SELECT "shopapp_productimage"."id",
"shopapp_productimage"."product_id",
"shopapp_productimage"."image",
"shopapp_productimage"."description" FROM "shopapp_productimage" WHERE "shopapp_productimage"."product_id" IN (2); args=(2,); alias=default

select "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."crested_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview" from "shopapp_product" where "shopapp_product"."id" = 2 LIMIT 21; args=(2,); alias=default
SELECT "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."description" FROM "shopapp_productimage" WHERE "shopapp_productimage"."product_id" IN (2); args=(2,); alias=default
SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_session"."expire_date" > '2024-03-04 09:49:38.984954' AND "django_session"."session_key" = 'akumc6z4s1xacgdjh9gzniol77ssndsg') LIMIT 21; args=('2024-03-04 09:49:38.984954', 'akumc6z4s1xacgdjh9gzniol77ssndsg'); alias=default
SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 1 LIMIT 21; args=(1,); alias=default
SELECT "shopapp_order"."id", "shopapp_order"."delivery_address", "shopapp_order"."promocode", "shopapp_order"."crested_at", "shopapp_order"."user_id", "shopapp_order"."receipt", "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "shopapp_order" INNER JOIN "auth_user" ON ("shopapp_order"."user_id" = "auth_user"."id"); args=(); alias=default
select ("shopapp_order_products"."order_id") as "_prefetch_related_val_order_id", "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."crested_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview" from "shopapp_product" inner join "shopapp_order_products" on ("shopapp_product"."id" = "shopapp_order_products"."product_id") where "shopapp_order_products"."order_id" in (1, 2) order by "shopapp_product"."price" asc, "shopapp_product"."name" asc; args=(1, 2); alias=default

