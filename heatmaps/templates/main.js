// Landing Page
class LandingPage extends React.Component {
  render() {
    return (
      <div className="hero is-fullheight is-primary">
        <div className="columns is-centered">
          <div className="column is-half">

            <div className="block has-background-primary my-4">
              <div className="is-size-1 has-text-centered is-italic has-text-weight-bold has-text-warning">
                HEATMAPS
              </div>
            </div>

            <StartBtn />
          </div>
        </div>
      </div>
    )
  }
}

function StartBtn(props) {
  return (
    <div className="my-6 has-text-centered">
      <button className="button is-warning is-size-2">
        Get Started &gt;
      </button>
    </div>
  )
}

// MainApp
class MainApp extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return(
      <LandingPage />
    )
  }
}

// ========================================

ReactDOM.render(<MainApp />, document.getElementById("root"));
