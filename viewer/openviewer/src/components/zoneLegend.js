import { h, Component } from 'preact';

import Key from './key';

export default class ZoneLegend extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        let zoneLegendStyle = {
            display: 'flex',
            flexDirection: 'column',
            // justifyContent: 'space-around',
            flexWrap: 'wrap',
            position: 'absolute',
            bottom: '15px',
            left: '20px',
            width: '200px',
            height: '160px'
        }

        if (this.props.keys.length <= 0) {
            zoneLegendStyle.display = 'none';
        }

        let keys = this.props.keys.map(key => {
            return <Key name={key.name} color={key.color}></Key>
        })

        return (
            <div id="zone-legend" style={zoneLegendStyle} className="sub-container-border">
                { keys }
            </div>
        )
    }
}