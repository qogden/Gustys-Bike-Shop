var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.totals = [];

    $scope.cartqty = function cartqty(qty, pid){
        $scope.qty=qty;
        $scope.pid=pid;
        socket.emit('cartqty', $scope.pid, $scope.qty);
        console.log('adjusting quantity');
    };
    
    $scope.addToCart = function addToCart(){
        console.log('enter')
        socket.emit('addToCart', $scope.qty);
        console.log('adjusting quantity');
    };
    
    $scope.itemspage = function itemspage(productid){
        socket.emit('single', productid);
        console.log('redirect to items page');
    };
    
    socket.on('totals', function(totals){
        $scope.totals = totals;
        $scope.$apply();
    });
    
    socket.on('added', function(){
        console.log('added to cart');
        
    });
    
    socket.on('connect', function(){
        console.log('connected');
        
    });
    
    
});