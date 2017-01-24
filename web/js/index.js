angular.module('app', []).controller('index', index);

function index($scope, $http) {
    $scope.request = {};
    $scope.state = 0;
    $scope.action = "";
    $scope.select_state = "";
    $scope.insert_state = "";
    $scope.delete_state = "";
    $scope.response = {};
    $scope.response_is_empty = true;

    $scope.set_response = function (data) {
        data = data || {};
        $scope.response = data;
        if ( is_empty(data) ) {
            $scope.response_is_empty = true;            
        } else {
            $scope.response_is_empty = false;
        }
    }

    $scope.send_get = function (route) {
        $http({
            url: window.location.origin + route,
            method: 'GET',
            data: $scope.request
            }).success(function(data) {
                if ( !is_empty(data) ) {
                    $scope.set_response(data);
                } else {
                    alert("No data found");
                }
                
            })
            .error(function(data) {
                console.log("Error on request: " + method + " ( " + data + " ) ");
            });
    }

    $scope.send_insert = function (route) {
        $http({
            url: window.location.origin + route,
            method: 'PUT',
            data: $scope.request
            }).success(function(data) {
                console.log(data);
                if (data['cpf'] == null){
                    alert("Problem inserting " + $scope.request['cpf']);
                } else {
                    alert("Person " + data['cpf'] + " inserted");
                }
            })
            .error(function(data) {
                console.log("Error on request: " + method + " ( " + data + " ) ");
            });
    }

    $scope.send_delete = function (route) {
        $http({
            url: window.location.origin + route,
            method: 'DELETE',
            data: $scope.request
            }).success(function(data) {
                if (data == 0){
                    alert("DB Cleaned");
                } else {
                    alert("Person " + data['cpf'] + " deleted.");
                }
            })
            .error(function(data) {
                console.log("Error on request: " + method + " ( " + data + " ) ");
            });
    }

    $scope.do_request = function () {
        var route = '/db/person';
        var cpf = $scope.request.cpf;
        if($scope.action == 'select') {
            route = check_route(route, cpf);
            $scope.send_get(route);
        } else if ($scope.action == 'insert') {
            $scope.send_insert(route);
        } else if ($scope.action == 'delete') {
            route = check_route(route, cpf);
            $scope.send_delete(route);
        } else {
            alert("Nothing to do");
        }
    }

    $scope.change_selector = function (select) {
        if(select == 'select') {
            $scope.select_state = "btn-primary";
            $scope.insert_state = "";
            $scope.delete_state = "";
            $scope.action = "select";
            $scope.state = 1;
        } else if (select == 'insert') {
            $scope.select_state = "";
            $scope.insert_state = "btn-primary";
            $scope.delete_state = "";
            $scope.action = "insert";
            $scope.state = 2;
            $scope.set_response();
        } else if (select == 'delete') {
            $scope.select_state = "";
            $scope.insert_state = "";
            $scope.delete_state = "btn-primary";
            $scope.action = "delete";
            $scope.state = 1;
            $scope.set_response();
        } else {
            $scope.select_state = "";
            $scope.insert_state = "";
            $scope.delete_state = "";
            $scope.action = "";
            $scope.state = 0;
            $scope.request = {};
            $scope.set_response();
        }
    }
}

function check_route(route, cpf) {
    if(cpf != "*") {
        return route + '/' + cpf;
    }
    return route;
}

function is_empty(obj) {
  return Object.keys(obj).length === 0;
}