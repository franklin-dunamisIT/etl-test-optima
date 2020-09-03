<?php

namespace App;

//use Illuminate\Database\Eloquent\Model;

// Need this to access the products from the Mongodb collection
use Jenssegers\Mongodb\Eloquent\Model; //as Eloquent;

class Product extends Model
{
    // connection for mongo
    protected $connection = 'mongodb';

    //  db collection for the critical products
    protected $collection = 'products';


    protected $fillable = ['name', 'available_qty'];
}
