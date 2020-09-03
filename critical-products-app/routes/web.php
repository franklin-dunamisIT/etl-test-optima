<?php
use App\Product;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Route http://127.0.0.1:8000/products to index function in the ProductController to display the products details
Route::get('/products', 'ProductController@index');


//Route::resource('products', 'ProductController');

Route::get('/', function () {
    return view('welcome');
});
