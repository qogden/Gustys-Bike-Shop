var App = angular.module('App', []);

App.controller('AppController', function($scope){
    var socket = io.connect('https://' + document.domain + ':' + location.port);

    $scope.cartqty = function cartqty(qty, pid){
        $scope.qty=qty
        $scope.pid=pid
        socket.emit('cartqty', $scope.pid, $scope.qty);
        console.log('adjusting quantity');
    };
    
    socket.on('adjustedqty', function(){
        console.log('adjusted quantity');
    });
    
    
    socket.on('connect', function(){
        console.log('connected');
    });
    
});