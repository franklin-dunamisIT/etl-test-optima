
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Product Index Page</title>
    <style>
        <style>
            th {
            height: 50px;
            }

            #product-table, #title{
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 70%;
            text-align: center;
            padding-left: 12px;
            }

            #product-table td, th {
            border: 1px solid #ddd;
            padding: 8px;
            }
            
            #product-table tr:nth-child(even){background-color: #f2f2f2;}

            #product-table tr:hover {background-color: #ddd;}

            #product-table th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #4CAF50;
            color: white;
            }
</style>

    </style>
  </head>
  <body>
    <div> Last updated: 
      <?php
    // Auto refresh every 30 min to ensure we have latest data from the source web page which is polled every 10-120secs
      $url=$_SERVER['REQUEST_URI'];
      header("Refresh: 30; URL=$url");
      echo date("Y-m-d h:i:sa", strtotime('now'))
    ?>
    </div>
    <div >
      <h2 id="title"> Critical Products</h2>
      <table id="product-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Quantity Available</th>
             
          </tr>
        </thead>
  
        <tbody>
      
          @foreach( $products as $product)
          <tr> 
            <td>{{$product->name}}</td>
            <td>{{$product->available_qty}}</td> 
           
          @endforeach
         </tbody>
       </table>
    </div>
  </body>

<footer>
 
</footer>
</html>

 
