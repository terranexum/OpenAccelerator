import { h, Component } from 'preact';

// import cytoscape from './lib/cytoscape.min';
import cytoscape from 'cytoscape';

import cydagre from 'cytoscape-dagre';
import popper  from 'cytoscape-popper';
import navigator from 'cytoscape-navigator';

import tippy from 'tippy.js';

// import undoRedo from 'cytoscape-undo-redo';

//import jquery from 'jquery';
// import expandCollapse from 'cytoscape-expand-collapse';

import { getCurrentStep } from '../utils/stepUtils'

cytoscape.use(cydagre);
cytoscape.use(popper);
navigator(cytoscape);

// cydagre(cytoscape);

// undoRedo(cytoscape);
// expandCollapse(cytoscape, jquery);

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
                name: 'dagre',
                directed: false,
                rankDir: 'TB',
                // ranker: 'tight-tree'
                animate: true,
                animationDuration: 250
            },

            style: [
                {
                    selector: '[fname]',
                    style: {
                        'height': 125,
                        'width': 175,
                        'background-color': 'data(zone)',
                        'color': '#cccccc',
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

            elements: this.props.graphData
        });

        this.cy.fit(this.cy.elements(), 20);
        this.cy.center();

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