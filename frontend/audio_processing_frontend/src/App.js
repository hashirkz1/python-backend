import React from 'react'
import Home from './Components/Home';
import UploadAudio from './Components/UploadAudio';
import Liverecording from './Components/Liverecording';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";


function App() {
  return (
    <>
      <Router>
          <div className='container'>
            <Switch>
                <Route exact path="/">
                  <Home/>
                </Route>
                <Route exact path="/modeltrain">
                  <UploadAudio/>
                </Route>
                <Route exact path="/liverecording">
                  <Liverecording/>
                </Route>
            </Switch>
          </div>
      </Router>
    </>
  )
}

export default App