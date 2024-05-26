
function downloadImages(){
          var coordinates = []
          var table = document.getElementById("imageTable");
          for (var i = 1, row; row = table.rows[i]; i++) {
            if (row.cells[0].getElementsByTagName("input")[0].checked){
              coordinates.push({"lat": row.cells[1].innerText,
                                  "lon": row.cells[2].innerText})
                }
            }

          const jsonData = JSON.stringify(coordinates);
          fetch('/export', {
                  method: 'POST', // Use POST for sending data
                  headers: {
                    'Content-Type': 'application/json' // Specify JSON content type
                  },
                  body: jsonData
                })
                .then(response => {
                  if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                  }
                  return response.blob(); // Get the response as a Blob (binary data)
                })
                .then(blob => {
                  const url = window.URL.createObjectURL(blob); // Create a temporary URL for the Blob

                  // Create a link element (invisible)
                  const link = document.createElement('a');
                  link.href = url;
                  link.setAttribute('download', `export-${Date.now()}.zip`); // Set a default filename

                  // Simulate a click on the link to trigger download
                  link.click();

                  // Clean up the temporary URL (optional)
                  window.URL.revokeObjectURL(url);
                })
                .catch(error => {
                  console.error('Error:', error);
                });

        }
function tableImages(lat, lon, text) {
            var tbodyRef = document.getElementById('imageTable').getElementsByTagName('tbody')[0];
            var newRow = tbodyRef.insertRow();

            var checkBoxCell = newRow.insertCell();
            var checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = true;
            checkBoxCell.appendChild(checkbox);

            var latCell = newRow.insertCell();
            var newLat = document.createTextNode(lat);
            latCell.appendChild(newLat);

            var lonCell = newRow.insertCell();
            var newLon = document.createTextNode(lon);
            lonCell.appendChild(newLon);

            var textCell = newRow.insertCell();
            var newText = document.createTextNode(text);
            textCell.appendChild(newText);
            /*
                var imageCell = newRow.insertCell();
                var imageTag = document.createElement("img");
                imageTag.src = "/image.png"
                imageCell.appendChild(imageTag);
            */
        }

            var map_50092ec2d670a75813efe362d308cc46 = L.map(
                "map_50092ec2d670a75813efe362d308cc46",
                {
                    center: [54.5, 21.1],
                    crs: L.CRS.EPSG3857,
                    zoom: 9,
                    zoomControl: true,
                    preferCanvas: false,
                    drawControl: true
                }
            );
            L.control.scale().addTo(map_50092ec2d670a75813efe362d308cc46);
            map_50092ec2d670a75813efe362d308cc46.on(L.Draw.Event.DRAWSTOP, e => {

                e.target.eachLayer(layer => {
                    if (layer.options.icon) {
                        tableImages(layer._latlng.lat, layer._latlng.lat, layer._tooltip._content);
                    }
                });

            });




            var tile_layer_64b6e4c62e37c4918a07ad44981b607b = L.tileLayer(
                "tiles/{z}/{x}/{y}.png",
                {"attribution": "OpenStreetMap", "detectRetina": false, "maxNativeZoom": 14, "maxZoom": 14, "minZoom": 9, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
            );


            tile_layer_64b6e4c62e37c4918a07ad44981b607b.addTo(map_50092ec2d670a75813efe362d308cc46);
            console.log(backendData);
             /*{% for record in data %}

            var marker_{{loop.index}} = L.marker(
                [{{ record[1] }}, {{record[2]}}],
                {}
            ).addTo(map_50092ec2d670a75813efe362d308cc46);


            marker_{{loop.index}}.bindTooltip(
                {{record[0]}},
                {"sticky": true}
            );

            {% endfor %}*/



            var options = {
              position: "topleft",
              draw: {"circle": false, "circlemarker": false, "marker": false, "polygon": false, "polyline": false, "rectangle": true},
              edit: {"cancel": false, "edit": true, "remove": true, "save": true},
            }
            // FeatureGroup is to store editable layers.
            var drawnItems_draw_control_426da795ecd07252d7cac96e37965514 = new L.featureGroup().addTo(
                map_50092ec2d670a75813efe362d308cc46
            );
            options.edit.featureGroup = drawnItems_draw_control_426da795ecd07252d7cac96e37965514;
            var draw_control_426da795ecd07252d7cac96e37965514 = new L.Control.Draw(
                options
            ).addTo( map_50092ec2d670a75813efe362d308cc46 );
            map_50092ec2d670a75813efe362d308cc46.on(L.Draw.Event.CREATED, function(e) {
                var layer = e.layer,
                    type = e.layerType;
                var coords = JSON.stringify(layer.toGeoJSON());
                var div = document.createElement("div");
                div.setAttribute("class", "rectangle_coords");
                div.setAttribute("coords", coords);
                document.body.append(div);

                layer.on('click', function() {
                    alert(coords);
                    console.log(coords);
                });
                drawnItems_draw_control_426da795ecd07252d7cac96e37965514.addLayer(layer);
             });
            map_50092ec2d670a75813efe362d308cc46.on('draw:created', function(e) {
                drawnItems_draw_control_426da795ecd07252d7cac96e37965514.addLayer(e.layer);
            });
