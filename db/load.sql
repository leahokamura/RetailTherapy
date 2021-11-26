\COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);
\COPY Product_Categories FROM 'data/Product_Categories.csv' WITH DELIMITER ',' NULL '' CSV                         
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Account FROM 'data/Account.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Reviews FROM 'data/Product_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sellers FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Inventory FROM 'data/Inventory.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM 'data/Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY InCart FROM 'data/InCart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SaveForLater FROM 'data/SaveForLater.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Orders FROM 'data/Orders.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerOrders FROM 'data/SellerOrders.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_Reviews FROM 'data/Seller_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Update_Submission FROM 'data/UpdateSubmission.csv' WITH DELIMITER ',' NULL '' CSV
\COPY PR_Comments FROM 'data/PR_Comments.csv' WITH DELIMITER ',' NULL '' CSV
