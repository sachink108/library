/*
 * @brief Control Panel controller definition
 */
'use strict';

app.controller('SearchController', ['$scope', '$http', '$timeout', '$rootScope', function($scope, $http, $timeout, $rootScope) {
    var searchScope=angular.element(document.querySelector('[id=search_ctrl]')).scope();
    var alertsScope = angular.element(document.querySelector('[id=alert_ctrl]')).scope();
    
    // refresh information periodically
    var POLLING_INTERVAL = 30 * 1000;
    var timer = null;
    
    // prevent refresh() being called twice simultaneously
    var inRefresh = false;
    var refresh = function() {
        // prevent overlap
        if (!inRefresh) {
            inRefresh = true;
            $scope.serverState = 'Busy';

            $scope.processList = [];
            $http({method:'GET', url:'http://localhost:9000/status', timeout: 5000})
                .success(function(data, status, headers, config) {
                    /*for (var program in data) {
                        if (data.hasOwnProperty(program)) {
                            if(data[program].hasOwnProperty('build_time')) {
                                var build_time = data[program]['build_time'];
                                var epochBuildTime = Number(build_time.substring(6,19));
                                var running_since = data[program]['running_since'];
                                var epochRunningTime = Number(running_since.substring(6,19));
                                var nSubscribers = data[program]['subscribers'] === null ? 0 : data[program]['subscribers'].length
                                var subscribers = data[program]['subscribers']
                                var mylist = []
                                for (var idx in subscribers) {
                                    var subName = data[program]['subscribers'][idx]['Value'].replace(/http\:\/\/localhost.*?\/(.*?)\/.*$/g, "$1");
                                    var subKey = data[program]['subscribers'][idx]['Key'];
                                    mylist.push({'subName': subName, 'subKey' : subKey});
                                }
                                $scope.processList.push({ 
                                    name: program, 
                                    status: data[program]['status'], 
                                    buildTime: (new Date(epochBuildTime)).toLocaleString(), 
                                    startedAt: (new Date(epochRunningTime)).toLocaleString(),
                                    nSubscribers: nSubscribers,
                                    subscribers: mylist
                                });
                            }
                            else {
                                $scope.processList.push({ name: program, status: data[program]['status'] });
                            }
                        }
                    }
                    */
                    inRefresh = false;
                    $scope.serverState = 'ready';
                    if(timer !== null)
                        clearInterval(timer);
                    timer = setInterval(refresh, POLLING_INTERVAL);
                })
                .error(function(data, status, headers, config) {

                    console.log("error");
                    inRefresh = false;
                    $scope.serverState = 'dead';
                });
        }
    };

    var search = function(searchTerms) {
        $scope.search_terms = searchTerms;
        //console.log("search terms are " + $scope.search_terms);
        $scope.docSelected = null;
        $scope.documentList = [];
        $http({method:'GET', url:'http://localhost:9000/search/' + $scope.search_terms, timeout: 5000})
            .success(function(data, status, headers, config) {
            console.log(data);
            for (var idx in data.result) {
                $scope.documentList.push(data.result[idx]);
            }
            console.log($scope.documentList);
        })
            .error(function(data, status, headers, config) {
                console.log("error");
                inRefresh = false; 
                $scope.serverState = 'dead';
            });
    };
    
    var loadDocument = function(doc) {
        $scope.docSelected = 1;
        //console.log("Will load document " + doc);
        $http({method:'GET', url:'http://localhost:9000/getdoc/' + doc, timeout: 5000})
            .success(function(data, status, headers, config) {
            //console.log(data);
            $scope.file_content = data.filecontent.replace($scope.$search_terms, "<b>$scope.search_terms</b>");
        })
            .error(function(data, status, headers, config) {
                console.log("error");
            });
    }

    // attempt to start
    var startProcess = function(processName) {

        for(var index=0; index < $scope.processList.length; ++index) {
            if ($scope.processList[index]['name'] === processName) {
                $scope.processList[index]['status'] = 'Starting';
                break;
            }
        }

        $http({ method: 'GET', url: 'http://ai-ml-dev.cloudapp.net:'+ portselectionScope.backendPort +'/start/' + processName })
            .success(function(data, status, headers, config) {

                if (data['program'] === processName) {
                    // request a refresh
                    $timeout($scope.refresh, 2000);
                }
                else {
                    console.log("ERROR[start]: received response for " + data['program'] + " instead of " + processName);
                }
            })
            .error (function(data, status, headers, config) {
                console.log('error');
            });
    };

    var unsubscribeProcess = function(processName, subscriber, subKey) {
        console.log("UnsubscribeProcess Received = " + processName + " " + subKey);
        var r = "process=" + processName + ",subkey=" + subKey;
        
        $http({method: 'POST', url: 'http://localhost:' + portselectionScope.backendPort + '/unsubscribe/' + r})
            .success(function(data) {
                //console.log(data);
                if(data.status === 'OK') {
                  console.log("Unsubscribed " + subscriber + " from " + processName); 
                }
                else {
                    alertsScope.addAlert("Error: " + subscriber + ' could not be unsubscribed');
                }
            })
            .error(function(data) {
                alertsScope.addAlert("Error: " + subscriber + ' could not be unsubscribed');
            });
    };
    
    // attempt to restart
    var restartProcess = function(processName) {

        for(var index=0; index < $scope.processList.length; ++index) {
            if ($scope.processList[index]['name'] === processName) {
                $scope.processList[index]['status'] = 'Restarting';
                break;
            }
        }

        var url='http://localhost:'+ portselectionScope.backendPort +'/force-restart/' + processName;
        $http({ method: 'GET', url: url })
            .success(function(data, status, headers, config) {

                if (data['program'] === processName) {
                    // request a refresh
                    $timeout($scope.refresh, 5000);
                }
                else {
                    console.log("ERROR[start]: received response for " + data['program'] + " instead of " + processName);
                }
            })
            .error (function(data, status, headers, config) {
                console.log('error calling ' + url);
            });
    };

    // attempt to stop
    var stopProcess = function(processName) {

        for(var index=0; index < $scope.processList.length; ++index) {
            if ($scope.processList[index]['name'] === processName) {
                $scope.processList[index]['status'] = 'Stopping';
                break;
            }
        }

        var url='http://localhost:'+ portselectionScope.backendPort +'/stop/' + processName;
        $http({ method: 'GET', url: url })
            .success(function(data, status, headers, config) {

                if (data['program'] === processName) {
                    // request a refresh
                    $timeout($scope.refresh, 2000);
                }
                else {
                    console.log("ERROR[stop]: received response for " + data['program'] + " instead of " + processName);
                }
            })
            .error (function(data, status, headers, config) {
                console.log('error accessing ' + url);
            });
    };
    
    var toggleDropdown = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.status.isopen = !$scope.status.isopen;
    };
    
    $scope.documentList     = [];
    $scope.search_terms     = null;
    $scope.search           = search;
    $scope.loadDocument     = loadDocument;
    $scope.docSelected      = null;
    $scope.file_content     = null;
    $scope.refresh          = refresh;
    $scope.serverState      = 'initializing';
    $scope.status           = { isopen: false };
    $scope.toggleDropdown   = toggleDropdown;

    // =======================================================================================================
    // close any open websockets
    if ($rootScope.ws) {
        $rootScope.ws.close();
        $rootScope.ws = null;
    }

    // start it off
    $scope.refresh();
}]);

