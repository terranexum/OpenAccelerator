import { h, Component } from 'preact';

export default class Key extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        let keyStyle = {
            width: 'calc(50% - 5px)',
            backgroundColor: this.props.color,
            padding: '5px',
            border: '1px solid ' + this.props.color,
            borderRadius: '3px',
            margin: '5px'
        }

        return (
            <div style={keyStyle}>
                <span id="key-name">{this.props.name}</span>
            </div>
        )
    }
}