'use strict';

app.controller('HomeController', ['$rootScope','$scope', '$uibModal', '$cookieStore', function ($scope, $rootScope, $uibModal, $cookieStore) {
    console.log("Home controller initialized");
    var globals = $cookieStore.get('globals');
    console.log(globals);
    $scope.username = globals.currentUser.username;
    $scope.toggle = true;
    $scope.showHide = "Show Categories";
    
    $scope.name = "Sachin";
    
    $scope.toggleCat = function() {
        $("#wrapper").toggleClass("toggled");
        $scope.showHide = $scope.showHide === "Show Categories" ? "Hide Categories" : "Show Categories";
    };
    
    $scope.readURL = function(input) {
        console.log("IN readURL");
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#blah').attr('src', e.target.result)
                    .width(150)
                    .height(200);
            };
            
            reader.readAsDataURL(input.files[0]);
        }
    };
    
    $scope.addBook = function() {
        console.log("Adding Book");
        
        var modalInstance = $uibModal.open({
          animation: $scope.animationsEnabled,
          templateUrl: 'addBook.html',
          controller: 'ModalInstanceCtrl',
        });
        modalInstance.result.then(function (selectedItem) {
            
        }, function () {
            console.log('Modal dismissed at: ' + new Date());
        });
    };
}]);

app.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance) {
  $scope.ok = function () {
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});