import { h, Component } from 'preact';

import Diagram from './diagram';
import ZoneLegend from './zoneLegend';

export default class DiagramArea extends Component {
    constructor(props) {
        super(props);
        // console.log(props);
    }

    render() {

        let dims = {};

        //this is a hack but it's ok
        if (this.props.stepData.length == 0 && window.self == window.top) {
            dims.width = 'calc(80vw - 30px)';
        } else if (this.props.stepData.length == 0 && window.self != window.top) {
            dims.width = 'calc(70vw - 30px)'
        } else {
            dims.width = 'calc(60vw - 30px)'
        }

        let diagramAreaStyle = {
            width: dims.width,
            height: 'calc(100% - 20px)',
            zIndex: '999'
        };

        let btnStyle = {
            position: 'absolute',
            left: '10px',
            top: '60px',
            zIndex: 1000
        };

        return <div style={diagramAreaStyle}>
            <Diagram
                graphData={this.props.graphData}
                stepData={this.props.stepData}
                curStep={this.props.curStep}
                updateSelectedNode={this.props.updateSelectedNode}
                zoneData={this.props.zoneData}
                dims={dims}
                ref={(d) => {this.diag = d; }}
            />
            <button style={btnStyle} onClick={() => {this.diag.renderDiagram();}}> redraw </button>
        </div>
    }
}

