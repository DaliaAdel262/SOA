<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Checkout</title>
</head>
<body>
    <h1>Place Your Order</h1>
    
    <form href="confirmation.jsp" method="post">
        <div>
            <label>Customer ID:</label>
            <input type="number" name="customer_id" value="1" required>
        </div>
        
        <div>
            <label>Product ID:</label>
            <input type="number" name="product_id" value="1" required>
        </div>
        
        <div>
            <label>Quantity:</label>
            <input type="number" name="quantity" value="1" required>
        </div>
        
        <button type="submit">Place Order</button>
    </form>
    
    <a href="index.jsp"><button>Back to Catalog</button></a>
</body>
</html>