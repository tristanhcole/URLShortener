import React from 'react';

export default class LinkShortener extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      date: new Date(),
      value: '',
      link: '',
      loading: false,
      error: false,
    };
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }


  getShortLink() {
    const { value } = this.state;
    let data = {
      dest: value
    };
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        },
    };

    this.setState({ loading: true }, () => {
      fetch('/api/v1/shortlink', fetchData)
        .then(response => {
          if (response.status >= 400 && response.status <= 500) {
            this.setState({
              error: true
            })
          } else {
            this.setState({
              error: false
            })
          }
          return response.json()
        })
        .then(data => {
          this.setState({
            loading: false,
            link: data.link,
            message: data.message
          })
        })
    });
  }

  render() {

    let message = this.state.error ? this.state.message : this.state.link;
    return (
      <section className="hero is-fullheight">
        <div className="hero-body">
        <div className="container">
          <div className="notification">
            <div className="field has-addons has-addons-fullwidth is-large">
              <div className="control">
                <input
                  className="input is-large"
                  type="text"
                  placeholder="Link"
                  readOnly={this.state.loading}
                  value={this.state.value}
                  onChange={this.handleChange.bind(this)}
                  onKeyPress={event => {
                    if (event.key === 'Enter') {
                      this.getShortLink()
                    }
                  }}
                />
              </div>
              <div className="control">
                <a className={"button is-info is-large is-fullwidth" + (this.state.loading?' is-loading':'')} onClick={this.getShortLink.bind(this)}>
                  Shorten
                </a>
              </div>
            </div>
          </div>
          <div className={"notification is-light" + (this.state.error?' is-danger':' is-success') + (message === '' ? ' is-hidden' : '')}>
            <p><strong>{message}</strong></p>
          </div>

        </div>
      </div>
    </section>
    );
  }
}
