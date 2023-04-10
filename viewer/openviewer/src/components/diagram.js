import { h, Component } from 'preact';

// import cytoscape from './lib/cytoscape.min';
import cytoscape from 'cytoscape';

import cydagre from 'cytoscape-dagre';
import popper  from 'cytoscape-popper';
import navigator from 'cytoscape-navigator';


import cosebilkent from 'cytoscape-cose-bilkent';

import cise from 'cytoscape-cise';

import tippy from 'tippy.js';

// import undoRedo from 'cytoscape-undo-redo';

import jquery from 'jquery';
import expandCollapse from 'cytoscape-expand-collapse';
// import expandCollapse from 'cytoscape-expand-collapse';

import { getCurrentStep } from '../utils/stepUtils'

cytoscape.use(cydagre);
cytoscape.use(popper);
navigator(cytoscape);
//cytoscape.use(expandcollapse);
cytoscape.use(cosebilkent);
cytoscape.use(cise);


// cydagre(cytoscape);

// undoRedo(cytoscape);
expandCollapse(cytoscape, jquery);

export default class Diagram extends Component {

    constructor(props) {
        super(props);
        this.renderDiagram = this.renderDiagram.bind(this);
        this.processStep = this.processStep.bind(this);
        this.transferStep = this.transferStep.bind(this);
        this.curStep = 0;
        this.highlighted_nodes = [];
    }

    componentDidMount() {
        this.renderDiagram();
    }

    componentDidUpdate(prevProps, prevState) {
        try {

            const curGraphData = Object.assign({}, this.props.graphData);
            const prevGraphData = Object.assign({},prevProps.graphData);

            // console.log(curGraphData);

            const extractNodeData = node => {
                const selectAttrs = ({ id, fname, zone, parent, info }) => ({ id, fname, zone, parent, info });
                node.data = selectAttrs(node.data);
                return node;
            };

            const extractEdgeData = edge => {
                const selectAttrs = ({ id, source, target }) => ({ id, source, target});
                edge.data = selectAttrs(edge.data)
                return edge;
            }

            curGraphData.nodes = curGraphData.nodes.map(extractNodeData);
            curGraphData.edges = curGraphData.edges.map(extractEdgeData);

            prevGraphData.nodes = prevGraphData.nodes.map(extractNodeData);
            prevGraphData.edges = prevGraphData.edges.map(extractEdgeData);

            const curGraphDataStr = JSON.stringify(curGraphData);
            const prevGraphDataStr = JSON.stringify(prevGraphData);

            // console.log(curGraphDataStr, "\n", prevGraphDataStr);
            // console.log(previousGraphData);
            if (curGraphDataStr !== prevGraphDataStr) {
                this.renderDiagram();
            } else {
                this.transferStep(this.props.curStep);
            }
        } catch (e) {
            // this.renderDiagram();
            if (e instanceof TypeError) {

            }
            console.error(e);
        }
    }

    renderDiagram() {
        let that = this;

        

        this.cy = null;
        this.cy = cytoscape({
            container: that.base,

            boxSelectionEnabled: false,
            autounselectify: true,
            panningEnabled: true,
            userPanningEnabled: true,
            userZoomingEnabled: true,

            layout: {
                name: 'cise', // was dagre
                //directed: true,
                //rankDir: 'TB',
                // ranker: 'tight-tree'
                animate: false,
                animationDuration: 250,
                clusters: zones,
                 // -------- Optional parameters --------
                // Whether to animate the layout
                // - true : Animate while the layout is running
                // - false : Just show the end result
                // - 'end' : Animate directly to the end result
                //animate: false,
                
                // number of ticks per frame; higher is faster but more jerky
                refresh: 10, 
                
                // Animation duration used for animate:'end'
                //animationDuration: undefined,
                
                // Easing for animate:'end'
                animationEasing: undefined,
                
                // Whether to fit the viewport to the repositioned graph
                // true : Fits at end of layout for animate:false or animate:'end'
                fit: true,
                
                // Padding in rendered co-ordinates around the layout
                padding: 30,
                
                // separation amount between nodes in a cluster
                // note: increasing this amount will also increase the simulation time 
                nodeSeparation: 12.5,
                
                // Inter-cluster edge length factor 
                // (2.0 means inter-cluster edges should be twice as long as intra-cluster edges)
                idealInterClusterEdgeLengthCoefficient: 1.4,
            
                // Whether to pull on-circle nodes inside of the circle
                allowNodesInsideCircle: false,
                
                // Max percentage of the nodes in a circle that can move inside the circle
                maxRatioOfNodesInsideCircle: 0.1,
                
                // - Lower values give looser springs
                // - Higher values give tighter springs
                springCoeff: 0.45,
                
                // Node repulsion (non overlapping) multiplier
                nodeRepulsion: 4500,
                
                // Gravity force (constant)
                gravity: 0.25,
                
                // Gravity range (constant)
                gravityRange: 3.8, 
            
                // Layout event callbacks; equivalent to `layout.one('layoutready', callback)` for example
                ready: function(){}, // on layoutready
                stop: function(){}, // on layoutstop
            },

            style: [
                {
                    selector: '[fname]',
                    style: {
                        'height': 125,
                        'width': 175,
                        'background-color': 'data(zone)',
                        'color': '#333333',
                        'content': e => e.data('fname') ? e.data('fname') : '',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'font-size': 18,
                        'shape': 'roundrectangle',
                        'border-width': '5px',
                        'border-color': e => e.data('zone'),
                        'text-wrap': 'wrap',
                        'text-max-width': 175,
                        'z-index': 20
                    }
                },
                {
                    selector: '$node > [fname]',
                    style: {
                        'height': 125,
                        'width': 175,
                        'background-color': 'data(zone)',
                        'content': e => e.data('fname') ? e.data('fname') : '',
                        'text-valign': 'top',
                        'text-halign': 'center',
                        'font-size': 18,
                        'shape': 'roundrectangle',
                        'border-width': '5px',
                        'border-color': e => e.data('zone'),
                        'z-index': 20
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'curve-style': 'bezier',
                        // 'haystack-radius': 0,
                        'width': 10,
                        'opacity': 0.5,
                        'line-color': '#888',
                        'target-arrow-shape': 'none',
                        'target-arrow-color': '#888',
                        'target-endpoint': 'inside-to-node',
                        'source-arrow-shape': 'none',
                        'source-arrow-color': '#888',
                        'source-endpoint': 'inside-to-node',
                        'z-index': 30
                        // 'mid-source-arrow-color': 'red',
                        // 'mid-source-arrow-fill': 'filled'
                    }
                },
                {
                    selector: '.highlighted',
                    style: {
                        'border-color': '#248bca',
                        // 'line-color': '#61bffc',
                        'transition-property': 'border-color',
                        'transition-duration': '0.25s',
                    }
                },
                {
                    selector: '.highlighted-to-target',
                    style: {
                        'border-color': '#248bca',
                        'line-color': '#248bca',
                        'transition-property': 'border-color, line-color, target-arrow-color',
                        'transition-duration': '0.25s',
                        'target-arrow-color': '#248bca',
                        // 'source-arrow-color': '#61bffc',
                        'target-arrow-shape': 'triangle',
                        // 'source-arrow-shape': 'none',
                        'target-endpoint': 'outside-to-node',
                        'arrow-scale': 1.5,
                        'opacity': 1
                    }
                },
                {
                    selector: '.highlighted-to-source',
                    style: {
                        'border-color': '#248bca',
                        'line-color': '#248bca',
                        'transition-property': 'border-color, line-color, source-arrow-color',
                        'transition-duration': '0.25s',
                        'source-arrow-color': '#248bca',
                        // 'source-arrow-color': '#61bffc',
                        'source-arrow-shape': 'triangle',
                        // 'source-arrow-shape': 'none',
                        'source-endpoint': 'outside-to-node',
                        'arrow-scale': 1.5,
                        'opacity': 1
                    }
                },
            ],

            defaultOptions: [ 
            {
                // Called on `layoutready`
                ready: function () {
                },
                // Called on `layoutstop`
                stop: function () {
                },
                // 'draft', 'default' or 'proof" 
                // - 'draft' fast cooling rate 
                // - 'default' moderate cooling rate 
                // - "proof" slow cooling rate
                quality: 'default',
                // Whether to include labels in node dimensions. Useful for avoiding label overlap
                nodeDimensionsIncludeLabels: true,
                // number of ticks per frame; higher is faster but more jerky
                refresh: 30,
                // Whether to fit the network view after when done
                fit: false,
                // Padding on fit
                padding: 10,
                // Whether to enable incremental mode
                randomize: true,
                // Node repulsion (non overlapping) multiplier
                nodeRepulsion: 4500,
                // Ideal (intra-graph) edge length
                idealEdgeLength: 500,
                // Divisor to compute edge forces
                edgeElasticity: 0.45,
                // Nesting factor (multiplier) to compute ideal edge length for inter-graph edges
                nestingFactor: 0.9,
                // Gravity force (constant)
                gravity: 0.25,
                // Maximum number of iterations to perform
                numIter: 2500,
                // Whether to tile disconnected nodes
                tile: true,
                // Type of layout animation. The option set is {'during', 'end', false}
                animate: 'end',
                // Duration for animate:end
                animationDuration: 500,
                // Amount of vertical space to put between degree zero nodes during tiling (can also be a function)
                tilingPaddingVertical: 10,
                // Amount of horizontal space to put between degree zero nodes during tiling (can also be a function)
                tilingPaddingHorizontal: 10,
                // Gravity range (constant) for compounds
                gravityRangeCompound: 1.5,
                // Gravity force (constant) for compounds
                gravityCompound: 1.0,
                // Gravity range (constant)
                gravityRange: 3.8,
                // Initial cooling factor for incremental layout
                initialEnergyOnIncremental: 0.5
            }
            ],

            elements: this.props.graphData
        });

        this.cy.fit(this.cy.elements(), 20);
        this.cy.center();

        let options = {
            layoutBy: null, // to rearrange after expand/collapse. It's just layout options or whole layout function. Choose your side!
            // recommended usage: use cose-bilkent layout with randomize: false to preserve mental map upon expand/collapse
            fisheye: true, // whether to perform fisheye view after expand/collapse you can specify a function too
            animate: true, // whether to animate on drawing changes you can specify a function too
            animationDuration: 1000, // when animate is true, the duration in milliseconds of the animation
            ready: function () { }, // callback when expand/collapse initialized
            undoable: true, // and if undoRedoExtension exists,
      
            cueEnabled: true, // Whether cues are enabled
            expandCollapseCuePosition: 'top-left', // default cue position is top left you can specify a function per node too
            expandCollapseCueSize: 12, // size of expand-collapse cue
            expandCollapseCueLineSize: 8, // size of lines used for drawing plus-minus icons
            expandCueImage: undefined, // image of expand icon if undefined draw regular expand cue
            collapseCueImage: undefined, // image of collapse icon if undefined draw regular collapse cue
            expandCollapseCueSensitivity: 1, // sensitivity of expand-collapse cues
            edgeTypeInfo: "edgeType", // the name of the field that has the edge type, retrieved from edge.data(), can be a function, if reading the field returns undefined the collapsed edge type will be "unknown"
            groupEdgesOfSameTypeOnCollapse : false, // if true, the edges to be collapsed will be grouped according to their types, and the created collapsed edges will have same type as their group. if false the collapased edge will have "unknown" type.
            allowNestedEdgeCollapse: true, // when you want to collapse a compound edge (edge which contains other edges) and normal edge, should it collapse without expanding the compound first
            zIndex: 999 // z-index value of the canvas in which cue ımages are drawn
        };

        

        this.cy.expandCollapse(options);
        let api = this.cy.expandCollapse('get');
        //api.collapseAll(options);

        // the default values of each option are outlined below:
        var defaults = {
            container: false // string | false | undefined. Supported strings: an element id selector (like "#someId"), or a className selector (like ".someClassName"). Otherwise an element will be created by the library.
          , viewLiveFramerate: 0 // set false to update graph pan only on drag end; set 0 to do it instantly; set a number (frames per second) to update not more than N times per second
          , thumbnailEventFramerate: 30 // max thumbnail's updates per second triggered by graph updates
          , thumbnailLiveFramerate: false // max thumbnail's updates per second. Set false to disable
          , dblClickDelay: 200 // milliseconds
          , removeCustomContainer: true // destroy the container specified by user on plugin destroy
          , rerenderDelay: 100 // ms to throttle rerender updates to the panzoom for performance
        };
        
        
        

        var nav = this.cy.navigator( defaults ); // get navigator instance, nav

        let nodes = this.cy.filter((ele, i, eles) => {
            return (ele.data('parent') != undefined);
        })

        let zones = this.cy.filter((ele, i, eles) => {
            return (ele.data('zones') != undefined);
        })

        let popperNodes = this.cy.filter((ele, i, eles) => {
            return (ele.data('parent') != undefined) && (ele.data('info') != undefined && ele.data('info') != "");
        });

        let parents = this.cy.filter((ele, i, eles) => {
            return (ele.data('parent') == undefined);
        })

        //if none of them have parents, that means no zones
        if (nodes.length == 0) {
            nodes = this.cy.filter((ele, i, eles) => {
                return (ele.data('parent') == undefined);
            })

            popperNodes = this.cy.filter((ele, i, eles) => {
                return (ele.data('parent') == undefined) && (ele.data('info') != undefined && ele.data('info') != "");
            })
        }

        let tippyMap = {};

        for (let i = 0; i < popperNodes.length; i++) {
            let popperNode = popperNodes[i];
            let c_rect = popperNode.popperRef().getBoundingClientRect();
            let content = document.createElement('div');
            content.innerHTML = popperNode.data('info');
            //console.log('pn data id', popperNode.data('id'))
                    
            tippyMap[popperNode.data('id')] = tippy(content, {
                getReferenceClientRect: () => ({
                    width: c_rect.width,
                    height: c_rect.height,
                    left: c_rect.left,
                    right: c_rect.right,
                    top: c_rect.top,
                    bottom: c_rect.bottom,
                }),
                
                allowHTML: true,
                interactive: true,
                trigger: 'manual'
            }) /*.tooltips[0];*/

            //tippyMap[popperNode.data('id')].show();
        }

        /*
        nodes.on('click', function(evt) {
            console.log('evt target id', evt, evt.target._private.data.id);
            that.props.updateSelectedNode(evt.target._private.data.id);
            // the only way I could get this tooltip to appear 
            // was with a timeout
            // TODO: find a better way to do this
            setTimeout(() => {
                // console.log(tippyMap[evt.target.id()]);
                tippyMap[evt.target._private.data.id].show();
            }, 250);
        })
        */
        
        nodes.on('click', function(evt) {
            //console.log('evt target id', evt.target.id())
            //let num_id = evt.target.id().charCodeAt(0) - 64
            //console.log('num id', num_id)
            that.props.updateSelectedNode(evt.target.id());
            
            // let instance = tippyMap[evt.target.id()] //.popper;
            //console.log('instance pre', instance)
            //console.log('popper html', tippyMap[evt.target.id()].popper)

            /*
            let cont = document.createElement('div');
            cont.innerHTML = tippyMap[evt.target.id()].popper;
            instance.setProps({
                allowHTML: true,
                interactive: true,
                delay: [100, null],
                
            })
            instance.setContent(cont);
            console.log('instance post', instance)
            */
            
        })
        

        // console.log(this.props.curStep);
        this.transferStep(this.props.curStep);
    }

    processStep(step) {
        //a bit of debugging

        let nodes = step.nodes.map(node => {
            return this.cy.filter((ele, i, eles) => ele.data('id') === node)[0]
        });

        this.highlighted_nodes = this.highlighted_nodes.concat(nodes);

        // console.log(nodes);

        nodes[0].addClass('highlighted');

        if (nodes.length == 1) {
            return;
        }

        let edges = this.cy.filter((ele, i, eles) => {
            if (ele.data('source') == step.nodes[0] &&
                ele.data('target') == step.nodes[1] ||
                ele.data('target') == step.nodes[0] &&
                ele.data('source') == step.nodes[1]) {
                return true;
            }
        });

        this.highlighted_nodes = this.highlighted_nodes.concat(edges);

        if (edges[0].data('source') == step.nodes[0]) {
            edges[0].addClass('highlighted-to-target');
        } else {
            edges[0].addClass('highlighted-to-source');
        }

        nodes[1].addClass('highlighted');
    }

    transferStep(stepNum) {

        //find the step
        const stepStr = ""+(this.props.curStep);
        const relevantStep = getCurrentStep(stepStr, this.props.stepData);

        this.highlighted_nodes.map(node => {
            node.removeClass('highlighted');
            node.removeClass('highlighted-to-target');
            node.removeClass('highlighted-to-source');
        })

        this.highlighted_nodes = [];

        if (stepNum >= 0 && relevantStep != null) {

            this.curStep = stepNum;
            this.processStep(relevantStep);
        }
    }

    render() {

        let style = {
            width: '100%',
            height: '100%'
        };

        if (this.props.dims && this.props.dims.width) {
            style.width = this.props.dims.width;
        }

        if (this.props.dims && this.props.dims.height) {
            style.height = this.props.dims.height;
        }

        return (
            <div id="cy" style={style} className="container-border"></div>
        )
    }
}