angular.module('takeWing').factory('webServices',['$http','$window',function($http,$window){
        return {
            getBooks : function(query){
                return  $http.get('/shelves/index/?s='+query).then(function(response){ //wrap it inside another promise using then
                            return response.data.rawdata;  //only return friends 
                        });
            },
            
            uploadBook : function(book_id){
                $http.get('/shelves/upload/?fileid='+book_id).then(function(response){ //wrap it inside another promise using then
                    if (response.authorize_url){
                    var popup = $window.open('response.authorize_url, '_blank');
                        setTimeout( function() {
                            if(!popup || popup.outerHeight === 0) {
                                //First Checking Condition Works For IE & Firefox
                                //Second Checking Condition Works For Chrome
                                alert("Popup Blocker is enabled! Please add this site to your exception list.");
                            } 
                            else{
                                //create focus listener
                            }
                        }, 250);
                    }
                    return response;  //only return friends 
                });
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