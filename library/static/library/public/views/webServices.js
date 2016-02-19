angular.module('takeWing').factory('webServices',['$http',function($http){
        return {
            getBooks : function(query){
                return  $http.get('/shelves/index/?s='+query).then(function(response){ //wrap it inside another promise using then
                            return response.data.rawdata;  //only return friends 
                        });
            },
            
            uploadBook : function(book_id){
                return  $window.open('/shelves/upload/?fileid='+book_id', '_blank');
            },
			
			getAutocomplete : function(query){
                return  $http.get('/shelves/auto/?s='+query).then(function(response){ //wrap it inside another promise using then
                            return response.data.result_list.map( function (result) {
                                return {
                                  value: result,
                                  display: result
                                };   
                            });
                });
            }
        }
    }])