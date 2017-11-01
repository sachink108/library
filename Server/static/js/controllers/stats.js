'use strict';

app.controller('StatsController', ['$scope', '$http','$rootScope', function($scope, $http, $rootScope) {
    var statsScope=angular.element(document.querySelector('[id=stats_ctrl')).scope();
    var searchScope=angular.element(document.querySelector('[id=search_ctrl]')).scope();
    $scope.serverState = 'ready'; //searchScope.serverState;
    $scope.docInfoList = [];
    $scope.pauseResumeCaption = "Show Crawler Info";
    $scope.paused = true;
    $scope.client=null;

    // called when the client connects
    function onConnect() {
        // Once a connection has been made, make a subscription and send a message.
      console.log("onConnect");
      $scope.client.subscribe("/garble");
      //var message = new Paho.MQTT.Message("Hello");
      //message.destinationName = "/garble";
      //$scope.client.send(message);
    }

    // called when the client loses its connection
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:"+responseObject.errorMessage);
        }
    }

    // called when a message arrives
    function onMessageArrived(message) {
        console.log("onMessageArrived:"+message.payloadString);
    }
    
    if ($scope.serverState == 'ready') {
        
        // Create a client instance
        // $scope.client = new Paho.MQTT.Client("127.0.0.1", 1883, "garble");
        $scope.client = new Paho.MQTT.Client("test.mosquitto.org", 8080, "garble");
        //$scope.client = new Paho.MQTT.Client("iot.eclipse.org", 1883, "garble_stats");
        //$scope.client = new Paho.MQTT.Client("ws://iot.eclipse.org/ws", 1883, "garble_stats");
        
        //$scope.client = new Paho.MQTT.Client("127.0.0.1", 1883, "garble_stats");
        //console.log($scope.client);

        // set callback handlers
        $scope.client.onConnectionLost = onConnectionLost;
        $scope.client.onMessageArrived = onMessageArrived;

        $scope.client.connect({onSuccess:onConnect}); // connect the client
        
        /*
        var client = new Messaging.Client(hostname, port, clientid);
 
        var options = {
            //connection attempt timeout in seconds
            timeout: 3,
            //Gets Called if the connection has successfully been established
            onSuccess: function () {
                alert("Connected");
            },
 
            //Gets Called if the connection could not be established
            onFailure: function (message) {
                alert("Connection failed: " + message.errorMessage);
            }
        };
        //Attempt to connect
        client.connect(options);
        */
 
        $scope.togglePause = function() {
            safeApply($scope, function() {
                $scope.paused = !$scope.paused;
                $scope.pauseResumeCaption = $scope.paused ? "Show Crawler Info" : "Hide Crawler Info";
                
            });
        };
        
        var showStats = function() {
            if(!$scope.paused) {
                safeApply($scope, function() {
                    console.log("In ShowStats()");
                    $scope.paused = !$scope.paused;
                    $scope.pauseResumeCaption = $scope.paused ? "Resume" : "Pause";
                });
            }
        };
    }
    $scope.docInfoList = [];
    $scope.showStats   = showStats;
}]);

