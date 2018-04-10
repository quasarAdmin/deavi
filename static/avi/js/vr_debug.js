
AFRAME.registerPrimitive('a-ocean', {
    defaultComponents: {
        ocean: {},
        rotation: {x: -90, y: 0, z: 0}
    },
    mappings: {
        width: 'ocean.width',
        depth: 'ocean.depth',
        density: 'ocean.density',
        color: 'ocena.color',
        opacity: 'ocean.opacity'
    }
});
