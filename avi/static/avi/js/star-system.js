/*
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
*/
var stars_data = {};

var load = function(stars){
    stars_data = stars;
};

AFRAME.registerComponent('star-system', {
    schema: {
        color: {
            type: 'string',
            default: "#FFF"
        },
        radius: {
            type: 'number',
            default: 300,
            min: 0,
        },
        depth: {
            type: 'number',
            default: 300,
            min: 0,
        },
        size: {
            type: 'number',
            default: 1,
            min: 0,
        },
        count: {
            type: 'number',
            default: 10000,
            min: 0,
        },
        texture: {
            type: 'asset',
            default: ''
        },
        c_time: {
            type: 'number',
            default: 0,
            min: 0,
        }
    },

    texture: {},

    update: function(){
        //let texture = {};
        if (this.data.texture){
            this.texture.transparent = true;
            this.texture.map = new THREE.TextureLoader().load(this.data.texture);
        }
        this.create_system();
    },
    
    remove: function(){
        this.el.removeObject3D('star-system');
    },

    create_system: function(){
        
        
        const system = new THREE.Geometry();
        
        /*const starMaterial_red = new THREE.PointsMaterial(Object.assign(this.texture,{
            color: "red", size: 2}));*/
        
        $.each(stars_data, function(key, value){
            if(value[0] > -5){
                //(x-xc)^2 + (y-cy)^2 + (z-cz)^2 < r^2
                system.vertices.push(new THREE.Vector3(value[0], value[1], value[2]));
            }
        });

        /*while(stars.vertices.length < this.data.count){
        stars.vertices.push(this.randomVectorBetweenSpheres(this.data.radius,
                                                                this.data.depth));
        }*/
        
        const starMaterial = new THREE.PointsMaterial(Object.assign(this.texture,{
            color: this.data.color,
            size: this.data.size}));
        this.el.setObject3D('star-system', new THREE.Points(system, starMaterial));
    },
    
    randomVectorBetweenSpheres: function(radius, depth){
        const randomRadius = Math.floor(Math.random() * 
                                        (radius + depth - radius + 1) + radius);
        return this.randomSphereSurfaceVector(randomRadius);
    },

    randomSphereSurfaceVector: function(radius){
        const theta = 2 * Math.PI * Math.random();
        const phi = Math.acos(2 * Math.random() - 1);
        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.sin(phi) * Math.sin(theta);
        const z = radius * Math.cos(phi);
        return new THREE.Vector3(x, y, z);
    },
    
    tick: function(t){
        var d_time = t - this.data.c_time;
        if (d_time > 4000){
            this.data.c_time = t;
            this.remove();
            this.create_system();
            //console.log(t/1000);
        }
    }
});

AFRAME.registerComponent('camera-listener', {
    tick: function(){
        //console.log("tick");
    }
});

$(document).ready(
    function(){
        var cam = document.querySelector('#camera');//$('#camera');
        console.log(cam);
        cam.addEventListener('componentchanged', function(ev){
            if(ev.detail.name !== 'position'){return;}
            var pos = new THREE.Vector3();
            pos.setFromMatrixPosition(this.object3D.matrixWorld);
            //console.log(pos);
            var star_system = $('#star-system');
            console.log(star_system);
            //star_system.remove();
            //star_system.();
        });
    }
);
