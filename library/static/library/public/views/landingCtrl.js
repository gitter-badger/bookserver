(function () {
   angular.module('takeWing').controller('landingCtrl', function (webServices, $scope, $timeout, $q, $log, $mdDialog, $mdToast, $mdMedia) {

      var self = this;
      self.simulateQuery = false;
      self.isDisabled = false;
      // list of `state` value/display objects
      self.getMatches = getMatches;
      self.selectedItemChange = selectedItemChange;
      self.searchTextChange = searchTextChange;
      $scope.loading = false;
      $scope.nocover = "/media/noimage.jpg"
      $scope.random = "<random> 20"
      
 
      // ******************************
      // Internal methods
      // ******************************
      // loads books 
      function searchCatalog(query) {
         $scope.loading = true;
         webServices.getBooks(query).then(function (response) {
            $scope.loading = false;
            $scope.books = response; //Assign data received to $scope.data
         });
      }

      // loads autocomplete suggestions
      function getMatches(text) {
         deferred = $q.defer();
         webServices.getAutocomplete(text).then(function (response) {
            deferred.resolve(response);
         });
         return deferred.promise;
      }
      
      // logging search text
      function searchTextChange(text) {
         $log.info('Text changed to ' + text);
      }

      //autocomplete call
      function selectedItemChange(item) {
         $log.info('Item changed to ' + JSON.stringify(item));
         searchCatalog(item);
      }

  

      //google toast
      var googleToast = function () {
         $mdToast.show(
            $mdToast.simple()
               .textContent('Your book was sent to Google Books!')
               .position('bottom right')
               .hideDelay(3000)
            );
      };
 
      //Kindle toast     
      var kindleToast = function () {
         $mdToast.show(
            $mdToast.simple()
               .textContent('Your book was sent to Kindle Books!')
               .position('bottom right')
               .hideDelay(3000)
            );
      };

      // book download toast
      $scope.downloadToast = function () {
         $mdToast.show(
            $mdToast.simple()
               .textContent('Your book download has started!')
               .position('bottom right')
               .hideDelay(3000)
            );
      };

      //Author dialog
      $scope.showAdvanced = function (ev, authorName) {
        var dialogBooks
         webServices.getBooks(authorName).then(function (response) {
            dialogBooks = response; //Assign data received to dialogBooks
         });
         console.log(dialogBooks)
         $mdDialog.show({
            locals: { name: authorName,
                      books: dialogBooks },
            controller: DialogController,
            templateUrl: angular_url + 'views/authorDialogTemp.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
         })
            .then(function (answer) {
               console.log(answer)
               $scope.status = 'You said the information was "' + answer + '".';
            }, function () {
               $scope.status = 'You cancelled the dialog.';
            });
      };

      //Epub and google file transfer dialog
      $scope.downloadDialog = function (ev, url) {
         $mdDialog.show({
            controller: DialogController,
            templateUrl: angular_url + 'views/download.dialog.temp.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
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
      }

      //Mobi or kindle file transfer dialog
      $scope.downloadDialog1 = function (ev, url) {
         $mdDialog.show({
            controller: DialogController,
            templateUrl: angular_url + 'views/download.dialog1.temp.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
         }).then(function (answer) {
            if (answer == 'Kindle') {
               kindleToast();
               console.log("kindle")
            } else if (answer == 'Download') {
               location.href = url
               $scope.downloadToast();
            }
         }, function () {
            $scope.status = 'You cancelled the dialog.';
         });
      };

      function DialogController($scope, $mdDialog, name, books) {
         $scope.name=name;
         $scope.authorBooks=books
         console.log("books", books)
         $scope.wiki = "http://en.wikipedia.org/wiki/" + name
         
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

   });
})();