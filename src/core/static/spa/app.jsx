
class Loading extends React.Component {
    render () {
        return (
            <h1>Loading...</h1>
        )
    }
}

class Root extends React.Component {
    state = {
        logged_in: false,
        user_profile: null,
        community_profiles: [],
        as_profile: {
            type: null,
            profile: null,
        },
    };

    constructor(props) {
        super(props);

        let _this = this;
        fetch('/api/', {
            credentials: "same-origin",
        })
            .then((response) => {
                console.log(response);
                if (response.ok) {
                    // Create profile or show main
                    _this.setState({logged_in: true});
                    fetch('/api/user_profile/?self=1', {
                        credentials: "same-origin",
                    })
                        .then((response) => {
                            console.log(response);
                            if (response.ok) {
                                response.json().then((data) => {
                                    _this.setState({user_profile: data[0]});
                                })
                            } else {
                                _this.setState({user_profile: null});
                                //TODO: get community_profiles
                                //FIXME: get them anyway no matter the user profile
                            }
                        })
                        .catch((err) => {
                            console.log(err);
                            alert("Network error");
                        })
                } else {
                    // TODO: Check if some other unrelated error
                    _this.setState({logged_in: false});
                }
            })
            .catch((err) => {
                console.log(err);
                alert('Network error');
            });
    }

    render () {
        if (this.state.logged_in) {
            if (this.state.user_profile != null) {
                return (<UserProfile profile={this.state.user_profile}/>);
            } else {
                //TODO: check community profiles
                return (<h1>Some shit</h1>);
            }
        } else {
            return (<Login />);
        }
    }
}

class Login extends React.Component {
    render() {
        var action_url = "/login/" + window.location.search;
        console.log(action_url);
        return (
            <form action={action_url} method="POST">
                <DjangoCSRF />
                <input type="text" name="username">
                </input>
                <input type="password" name="password">
                </input>
                <input type="submit">
                </input>
            </form>
        )
    }
}

class Register extends React.Component {
    render() {

    }
}

class CreateProfile extends React.Component {
    render() {

    }
}

class CreateUserProfile extends React.Component {
    render() {
        return (
            <h1>Create user profile</h1>
        )
    }
}

class CreateCommunityProfile extends React.Component {
    render() {

    }
}

class UserProfile extends React.Component {
    state = {
        user_profile: null,
    };

    constructor(props) {
        super(props);
        if (this.props.profile) {
            this.state = {
                user_profile: this.props.profile,
            };
            return;
        }
        var fetch_url;
        if (this.props.profile_id) {
            fetch_url = '/api/user_profile/?id=' + this.props.profile_id;
        } else {
            fetch_url = '/api/user_profile/?self=1'
        }
        let _this = this;
        console.log(fetch_url);
        fetch(fetch_url, {
            credentials: "same-origin",
        })
            .then((response) => {
                console.log(response);
                if (response.ok) {
                    response.json().then((data) => {
                        console.log(data);
                        _this.setState({user_profile: data[0]});
                    });
                } else {
                    _this.setState({user_profile: null});
                }
            })
            .catch((err) => {
                console.log(err);
                alert('Network error');
            });
    }
    // TODO: Props - profile-id, load profile in constructor
    render() {
        if (this.state.user_profile == null) {
            return (<h1>T_T</h1>)
        }
        return (
            <div>
                <h1>{this.state.user_profile.first_name} {this.state.user_profile.last_name}</h1>
                <p>{this.state.user_profile.birthday}</p>
                <p>{(this.state.user_profile.gender == true)?"Male":"Female"}</p>
            </div>
        )
    }
}

class DjangoCSRF extends React.Component {

    getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    render() {
        return (
            <input type="hidden" name="csrfmiddlewaretoken" value={ this.getCookie('csrftoken') }>
            </input>
        )
    }
}

ReactDOM.render(
    <Root />,
    document.getElementById('app')
);