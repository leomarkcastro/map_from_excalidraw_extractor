var svgMesh3d = require("svg-mesh-3d");
var parsePath = require("extract-svg-path").parse;

var mesh = svgMesh3d(svgPath, {
  // delaunay: false,
  clean: true,
  simplify: 90,
  // scale: 0.0025,
});

console.log(mesh);
