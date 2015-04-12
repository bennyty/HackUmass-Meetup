<?php
// copy file content into a string var
$courses = file_get_contents('http://yacs.me/api/4/courses/?year=2015');
$deptIds = file_get_contents('http://yacs.me/api/4/departments/');
// convert the string to a json object
$jCourses = json_decode($courses);
$jdIds = json_decode($deptIds);

$ids = $jdIds->result;
$idArray = array();
foreach ($ids as $id) {
    $idArray[$id->id] = $id->code;
}


$courses = $jCourses->result;
$newJSON["classes"] = array();
foreach ($courses as $course) {
    $tempJ = array("department" => $idArray[$course->department_id], "number" => $course->number, "name" => $course->name);
    array_push($newJSON["classes"], $tempJ);
}
echo json_encode($newJSON);

?>
