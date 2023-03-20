import { h, Component } from 'preact';

export default class Info extends Component {

    render() {

        let el;

        if (!this.props.flowTitle) {
            el = <div id="info" className="sub-container-border">
                <h2> Invalid Title! </h2>
            </div>
        } else {
            el = <div id="info" className="sub-container-border">
                <h2> {this.props.flowTitle} </h2>
            </div>
        }

        return el;
    }
}