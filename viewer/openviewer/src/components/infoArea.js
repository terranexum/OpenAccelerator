import { h, Component } from 'preact';

import Controls from './controls';
import TableOfContents from './tableOfContents';
import Info     from './info';


export default class InfoArea extends Component {

    render() {

        let width;

        if (this.props.stepData.length == 0 && window.self == window.top) {
            width = 'calc(20% - 30px)'
        } else if (this.props.stepData.length == 0 && window.self != window.top) {
            width = 'calc(30% - 30px)';
        } else {
            width = 'calc(40% - 30px)'
        }

        let infoAreaStyle = {
            width: width,
            height: 'calc(100% - 20px)',
            zIndex: '999',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'space-around'
        }

        const countSteps = (sum, step) => {
            if (step.type == "single") {
                return sum + 1;
            } else if (step.type == "group") {
                return step.steps.reduce(countSteps, sum);
            }
        }

        let stepNum = this.props.stepData.reduce(countSteps, 0);

        return (
            <div id="infoArea" style={infoAreaStyle} className="right-panel">
                <Info flowTitle={this.props.flowTitle}></Info>
                <TableOfContents updateStep={this.props.updateStep}
                                 stepData={this.props.stepData}
                                 curStep={this.props.curStep}
                                 selectedNode={this.props.selectedNode}></TableOfContents>
                
                <Controls curStep={this.props.curStep} 
                          stepNum={stepNum}
                          updateStep={this.props.updateStep}
                          updateData={this.props.updateData}></Controls>
            </div>
        )
    }
}

/*<div id="info" className="sub-container-border">info</div>*/