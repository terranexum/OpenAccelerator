import { h, Component } from 'preact';
import info from '../assets/icons/info.png';

export default class TocStep extends Component {

    constructor(props) {
        super(props);
        this.setStep = this.setStep.bind(this);
        this.toggleToolTip = this.toggleToolTip.bind(this);
        this.state = {
            showToolTip: false
        };
    }

    componentDidUpdate() {
        // console.log(!elementInViewport(this.elem));

        function isElementInContainer(el, container) {

            var el_rect = el.getBoundingClientRect();
            // console.log(el_rect);

            var cont_rect = container.getBoundingClientRect();
            // console.log(cont_rect);

            return (
                el_rect.top >= cont_rect.top &&
                el_rect.bottom <= cont_rect.bottom
            );
        }

        if (this.props.matches && !isElementInContainer(this.elem, document.getElementById("table-of-contents"))) {
            this.elem.scrollIntoView(false);
        }
    }

    setStep() {
        this.props.updateStep(this.props.step.id);
    }

    toggleToolTip() {
        this.setState({
            showToolTip: !this.state.showToolTip
        });
    }

    render() {

        let classNames = [];
        if (this.props.matches) {
            classNames.push("current-step-toc");
        }
        if (!this.props.related && this.props.filterRelated) {
            classNames.push("unrelated-step-toc");
        }

        if (window.self != window.top) {
            classNames.push("iframe-list-style");
        }

        const hasToolTip = this.props.step.note != undefined && this.props.step.note != "";
        let toolTip = null;
        let toolTipText = null;
        // console.log(this.props.step);
        if (hasToolTip) {
            classNames.push("hasnote");
            toolTip = (
                <span className="to-left" onClick={this.toggleToolTip}> <img src={info}></img> </span>
            );
            toolTipText = (
                <div className="note" dangerouslySetInnerHTML={{__html:this.props.step.note.replace(/\\n/g, "<br/>")}}> </div>
            )
        }

        return <li
            ref={(elem) => { this.elem = elem }}
            className={classNames.join(' ')}
            onclick={this.setStep} >
            {toolTip}
            <span> {this.props.step.description} </span><br/>
            {this.state.showToolTip ? toolTipText : null}
        </li>
    }
}