var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);
   
    $scope.cartrm = function cartrm(qty, pid){
        socket.emit('cartrm2', qty, pid);
        console.log('removing product');
    };
    
    $scope.cartqty = function cartqty(qty, pid){
        socket.emit('cartqty2', qty, pid);
        console.log('adjusting quantity');
    };
    
    socket.on('adjustedqty', function(){
        console.log('adjusted quantity');
    });
    
    socket.on('premove', function(){
        console.log('product removed');
    });
    
    socket.on('connect', function(){
        console.log('connected');
    });
    
});