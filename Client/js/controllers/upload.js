app.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
        var model = $parse(attrs.fileModel);
        var modelSetter = model.assign;
        element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

/*
app.service('fileUpload', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        console.log("Uploading file");
        $http({
            url: "http://localhost:8888",
            method: "POST",
            data: {'filename': '', 'content': '',
        }).then(function(data) {
            console.log("Received " + data);
        },
        function(data) {
            console.log("Failed");
        });
    };
});
*/
app.controller('uploadController', ['$scope', 'fileUpload', function($scope, fileUpload){
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' + file);
        console.dir(file);
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
}]);
