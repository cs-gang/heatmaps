
function Header(props) {
  return (<div className={props.class}>Header</div>)
}

function Body(props) {
  return (<div className={props.class}>Body</div>)
}

function MainApp(props) {
  return (
    <React.Fragment>
      <Header class="bg-orange-red" />
      <Body class="bg-gray-100" />
    </React.Fragment>
  )
}

ReactDOM.render(<MainApp />, document.getElementById('root'));
