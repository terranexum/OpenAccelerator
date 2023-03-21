import { h, Component } from 'preact';

import TocStep from './tocStep';

import { getCurrentStep } from '../utils/stepUtils'

export default class TableOfContents extends Component {

    constructor(props) {
        super(props);
    }

    render() {


        let tableOfContentsStyle = {
            overflowY: 'auto',
            overflowX: 'hidden'
        }

        const stepStr = ""+(this.props.curStep);
        const currentStep = getCurrentStep(stepStr, this.props.stepData);
        

        const flattenSteps = (steps) => {
            const flattened = [];

            steps.forEach(s => {
                if (s.type == "single") {
                    flattened.push(s);
                } else if (s.type == "group") {
                    flattened.push(...flattenSteps(s.steps));
                }
            });

            return flattened;
        }
        const flattenedSteps = flattenSteps(this.props.stepData);

        const filterRelated = flattenedSteps.filter(step => this.props.selectedNode != null &&
            step.nodes.includes(this.props.selectedNode)).length > 0;        


        const renderStep = (step) => {
            if (step.type == "single") {
                let matches = false;
                let related = false;
                if (this.props.selectedNode != null) {
                    related = step.nodes.includes(this.props.selectedNode);
                }
                matches = currentStep != null && step.id === currentStep.id;
                return <TocStep matches={matches}
                    filterRelated={filterRelated}
                    related={related}
                    step={step}
                    updateStep={this.props.updateStep}>
                </TocStep>
            } else if (step.type == "group") {
                return (
                    <li>
                        <span><i>({step.groupName})</i>   {step.description}</span>
                        <ol class="custom-list">
                            {step.steps.map(renderStep)}
                        </ol>
                    </li>
                );
            }

        }

        const stepLi = this.props.stepData.map(renderStep);

        let emptyMsg;
        let msgStyle = {
            textAlign: 'center'
        };

        if (stepLi.length == 0) {
            emptyMsg = <p style={msgStyle}> add steps to the JSON file if you want to step through a flow</p>
        } else {
            emptyMsg = null;
        }

        return (
            <div id="table-of-contents"
                style={tableOfContentsStyle}
                className="sub-container-border"
                ref={(div) => { this.scrolldiv = div }}>
                {emptyMsg}
                <ol class="custom-list">
                    {stepLi}
                </ol>
            </div>
        )
    }
}