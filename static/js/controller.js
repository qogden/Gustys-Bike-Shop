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
    
    socket.on('totals', function(totals){
        $scope.totals = totals;
        $scope.$apply();
    });
    
    
    socket.on('connect', function(){
        console.log('connected');
        
    });
    
});