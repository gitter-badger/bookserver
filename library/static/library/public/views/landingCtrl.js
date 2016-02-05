(function () {
   angular.module('takeWing').controller('landingCtrl', function (webServices, $scope, $timeout, $q, $log, $mdDialog, $mdToast, $mdMedia) {

      var self = this;
      self.simulateQuery = false;
      self.isDisabled = false;
      // list of `state` value/display objects
      self.getMatches = getMatches;
      self.selectedItemChange = selectedItemChange;
      self.searchTextChange = searchTextChange;
      self.newState = newState;
      
      function newState(state) {
         alert("Sorry! You'll need to create a Constituion for " + state + " first!");
      }
      // ******************************
      // Internal methods
      // ******************************

      function searchCatalog(query) {
         webServices.getBooks(query).then(function (response) {
            $scope.books = response; //Assign data received to $scope.data
         });
      }
      
      function getMatches(text) {
         deferred = $q.defer();
         webServices.getAutocomplete(text).then(function (response) {
            deferred.resolve(response);
         });
         return deferred.promise;
      }
      
      function searchTextChange(text) {
         $log.info('Text changed to ' + text);
      }
      
      function selectedItemChange(item) {
         $log.info('Item changed to ' + JSON.stringify(item));
         searchCatalog(item);
      }

      $scope.showConfirm = function (ev, url) {
         // Appending dialog to document.body to cover sidenav in docs app
         var confirm = $mdDialog.confirm()
            .title('Where would you like to send your book?')
            .textContent('')
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Google')
            .clickOutsideToClose(true)
            .cancel('Download');
         $mdDialog.show(confirm).then(function () {
            $scope.googleToast();
         }, function () {
            location.href = url
            $scope.downloadToast();
         });
      };

      var googleToast = function () {
         $mdToast.show(
            $mdToast.simple()
               .textContent('Your book was sent to Google Books!')
               .position('bottom right')
               .hideDelay(3000)
            );
      };

      $scope.downloadToast = function () {
         $mdToast.show(

            $mdToast.simple()
               .textContent('Your book download has started!')
               .position('bottom right')
               .hideDelay(3000)
            );
      };

      $scope.showAdvanced = function (ev, idx) {
         var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
         $mdDialog.show({
            locals: idx,
            controller: DialogController,
            templateUrl: angular_url+'views/authorDialogTemp.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: useFullScreen
         })
            .then(function (answer) {
               console.log(answer)
               $scope.status = 'You said the information was "' + answer + '".';
            }, function () {
               $scope.status = 'You cancelled the dialog.';
            });
            
         $scope.$watch(function () {
            return $mdMedia('xs') || $mdMedia('sm');
         }, function (wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
         });
      };

      $scope.downloadDialog = function (ev, url) {
         var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
         $mdDialog.show({
            controller: DialogController,
            templateUrl: angular_url+'views/download.dialog.temp.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: useFullScreen
         }).then(function (answer) {
            if (answer == 'Google') {
               googleToast();
               console.log("google")
            } else if (answer == 'Download') {
               location.href = url
               $scope.downloadToast();
            }
         }, function () {
            $scope.status = 'You cancelled the dialog.';
         });

         $scope.$watch(function () {
            return $mdMedia('xs') || $mdMedia('sm');
         }, function (wantsFullScreen) {
            $scope.customFullscreen = (wantsFullScreen === true);
         });

      };

      function DialogController($scope, $mdDialog) {

         var self = $scope;
         
         $scope.hide = function () {
            $mdDialog.hide();
         };
         $scope.cancel = function () {
            $mdDialog.cancel();
         };
         $scope.answer = function (idx) {
            $mdDialog.hide(idx);
         };
      }

   })
})();