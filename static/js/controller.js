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
    
    $scope.addToCart = function addToCart(pid){
        console.log(pid);
        console.log($scope.qty);
        socket.emit('addToCart', pid, $scope.qty);
        console.log('adding to cart');
    };
    

    $scope.itemspage = function itemspage(productid){
        socket.emit('single', productid);
        console.log('redirect to items page');
    };
    
    socket.on('totals', function(totals){
        $scope.totals = totals;
        console.log('totals', $scope.totals);
        $scope.$apply();
    });
    
    socket.on('connect', function(){
        console.log('connected');
        
    });
    
    
});