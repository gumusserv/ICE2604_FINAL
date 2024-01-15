"use strict";

const {
  Component,
  Children,
  PropTypes
} = React;
const {
  StaggeredMotion,
  Motion,
  spring
} = ReactMotion;

//Circled
const Circled = React.createClass({
  displayName: "Circled",
  getInitialState() {
    return {
      open: false,
      opacity: 1
    };
  },
  handleMouseOver() {
    this.setState({
      open: !this.state.open
    });
  },
  handleTouchStart(e) {
    e.preventDefault();
    this.handleMouseOver();
  },
  getStyles(prevStyles) {
    // we're using the previous style to update the next ones placement
    const endValue = prevStyles.map((_, i) => {
      let staggerStiff = 100,
        staggerDamp = 19;
      return i === 0 ? {
        opacity: spring(this.state.open ? 0 : 1, {
          stiffness: staggerStiff,
          damping: staggerDamp
        })
      } : {
        opacity: spring(this.state.open ? 0 : 1, {
          stiffness: staggerStiff - i * 7,
          damping: staggerDamp + i * 0.2
        })
      };
    });
    return endValue;
  },
  render() {
    const circNum = this.props.circNum || 5,
      classNum = this.props.classNum || "c1",
      circBk = this.props.circBk || "black",
      pathColor = this.props.pathColor || "#eaedef",
      settings = {
        stiffness: 200,
        damping: 20
      };
    const pathData = ["M48.8,0A48.8,48.8,0,1,0,97.6,48.8,48.8,48.8,0,0,0,48.8,0Zm0,88.6A39.8,39.8,0,1,1,88.6,48.8,39.8,39.8,0,0,1,48.8,88.6Z", "M48.8,9.1A39.8,39.8,0,1,0,88.6,48.8,39.8,39.8,0,0,0,48.8,9.1Zm0,67.9A28.1,28.1,0,1,1,77,48.8,28.1,28.1,0,0,1,48.8,77Z", "M48.8,20.7A28.1,28.1,0,1,0,77,48.8,28.1,28.1,0,0,0,48.8,20.7Zm0,50.1a22,22,0,1,1,22-22A22,22,0,0,1,48.8,70.8Z", "M48.8,26.8a22,22,0,1,0,22,22A22,22,0,0,0,48.8,26.8Zm0,39.1A17.1,17.1,0,1,1,66,48.8,17.1,17.1,0,0,1,48.8,66Z", "M48.8,31.7A17.1,17.1,0,1,0,66,48.8,17.1,17.1,0,0,0,48.8,31.7Zm0,29A11.9,11.9,0,1,1,60.7,48.8,11.9,11.9,0,0,1,48.8,60.7Z", "M48.8,36.9A11.9,11.9,0,1,0,60.7,48.8,11.9,11.9,0,0,0,48.8,36.9Zm0,19.9a8,8,0,1,1,8-8A8,8,0,0,1,48.8,56.8Z", "M48.8,40.8a8,8,0,1,0,8,8A8,8,0,0,0,48.8,40.8Zm0,12.6a4.6,4.6,0,1,1,4.6-4.6A4.6,4.6,0,0,1,48.8,53.5Z", "M48.8,44.2a4.6,4.6,0,1,0,4.6,4.6A4.6,4.6,0,0,0,48.8,44.2Zm0,7.1a2.5,2.5,0,1,1,2.5-2.5A2.5,2.5,0,0,1,48.8,51.3Z", "M51.3 48.8c0 1.38-1.12 2.5-2.5 2.5s-2.5-1.12-2.5-2.5 1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5z"];
    let arr = [];
    for (var i = 0; i < pathData.length; i++) {
      arr.push({
        opacity: 1
      });
    }
    return /*#__PURE__*/React.createElement("div", {
      onClick: this.handleMouseOver,
      onTouchStart: this.handleTouchStart,
      className: "circ-contain"
    }, /*#__PURE__*/React.createElement("div", {
      className: "circ-lg"
    }), /*#__PURE__*/React.createElement("div", {
      className: "circled back " + circBk
    }, "Lorem Ipsum Dolor Sit"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("svg", {
      className: "circled circle-svg",
      xmlns: "http://www.w3.org/2000/svg",
      viewBox: "0 0 97.6 97.6"
    }, /*#__PURE__*/React.createElement(StaggeredMotion, {
      defaultStyles: arr,
      styles: this.getStyles
    }, circ => /*#__PURE__*/React.createElement("g", {
      fill: pathColor,
      className: "cPath"
    }, circ.map(({
      opacity
    }, i) => /*#__PURE__*/React.createElement("path", {
      key: i,
      d: pathData[i],
      className: `things s${i}`,
      style: {
        opacity: opacity
      }
    }))))), /*#__PURE__*/React.createElement(Motion, {
      style: {
        op: spring(this.state.open ? 0 : 1, settings)
      }
    }, ({
      op
    }) => /*#__PURE__*/React.createElement("div", {
      className: "circled front " + classNum,
      style: {
        opacity: op
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "itals"
    }, "Printed"), /*#__PURE__*/React.createElement("h1", null, circNum)))));
  }
});

//App
const App = React.createClass({
  displayName: "App",
  render() {
    return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
      className: "pR"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stripe-vt"
    }), /*#__PURE__*/React.createElement("div", {
      className: "stripe-hz"
    })), /*#__PURE__*/React.createElement("div", {
      className: "container-fluid"
    }, /*#__PURE__*/React.createElement("div", {
      className: "row"
    }, /*#__PURE__*/React.createElement(ColumnOne, null), /*#__PURE__*/React.createElement(ColumnTwo, null), /*#__PURE__*/React.createElement(ColumnThree, null), /*#__PURE__*/React.createElement(ColumnFour, null))));
  }
});

//ColumnOne
const ColumnOne = React.createClass({
  displayName: "ColumnOne",
  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: "column  col-xs-16 col-xs-offset-3 col-sm-8 col-sm-offset-2  col-md-8 col-md-offset-2"
    }, /*#__PURE__*/React.createElement(Picture, null), /*#__PURE__*/React.createElement(Circled, null), /*#__PURE__*/React.createElement(PrintArea, {
      margin: "mt"
    }), /*#__PURE__*/React.createElement(Picture, {
      length: "short"
    }));
  }
});

//ColumnTwo
const ColumnTwo = React.createClass({
  displayName: "ColumnTwo",
  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: "column  col-xs-16 col-xs-offset-2 col-sm-8 col-sm-offset-1 col-md-8 col-md-offset-1"
    }, /*#__PURE__*/React.createElement(Circled, {
      classNum: "c2",
      circNum: "36"
    }), /*#__PURE__*/React.createElement(Picture, {
      picNum: "2"
    }), /*#__PURE__*/React.createElement(Text, null));
  }
});

//ColumnThree
const ColumnThree = React.createClass({
  displayName: "ColumnThree",
  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: "column  col-xs-16 col-xs-offset-3 col-sm-8 col-sm-offset-2 col-md-8 col-md-offset-2"
    }, /*#__PURE__*/React.createElement(Circled, {
      classNum: "c3",
      circNum: "12"
    }), /*#__PURE__*/React.createElement(Picture, {
      length: "short",
      picNum: "2"
    }), /*#__PURE__*/React.createElement(PrintArea, null), /*#__PURE__*/React.createElement(Picture, {
      picNum: "3",
      margin: "mt"
    }));
  }
});

//ColumnFour
const ColumnFour = React.createClass({
  displayName: "ColumnFour",
  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: "column  col-xs-16 col-xs-offset-2 col-sm-8 col-sm-offset-1 col-md-8 col-md-offset-1"
    }, /*#__PURE__*/React.createElement(Circled, {
      classNum: "c4",
      circNum: "2",
      circBk: "grey",
      pathColor: "black"
    }), /*#__PURE__*/React.createElement(Picture, {
      picNum: "4"
    }), /*#__PURE__*/React.createElement(Text, {
      grey: "grey"
    }));
  }
});

// Text
function Text(props) {
  const grey = props.grey || "sm-grey";
  return /*#__PURE__*/React.createElement("div", {
    className: grey
  }, /*#__PURE__*/React.createElement("h2", null, "Lorem Ipsum"), /*#__PURE__*/React.createElement("p", null, "Man braid iPhone locavore hashtag pop-up, roof party forage heirloom chillwave brooklyn yr 8-bit gochujang blog. Gastropub locavore crucifix."), /*#__PURE__*/React.createElement("button", {
    className: "slide"
  }, "See More \u27F6"));
}

// Picture
function Picture(props) {
  const picNum = props.picNum || 1,
    length = props.length || "long",
    margin = props.margin || "";
  return /*#__PURE__*/React.createElement("div", {
    className: length + " " + length + picNum + " " + margin
  });
}

// PrintArea
function PrintArea(props) {
  const margin = props.margin || "";
  return /*#__PURE__*/React.createElement("div", {
    className: "printArea " + margin
  }, /*#__PURE__*/React.createElement("div", {
    className: "printrow"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lg-top slide"
  }, /*#__PURE__*/React.createElement("span", {
    className: "itals"
  }, "Date "), "Picture"), /*#__PURE__*/React.createElement("div", {
    className: "sm-top slide"
  }, "Picture")), /*#__PURE__*/React.createElement("div", {
    className: "printrow"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sm-bot slide"
  }, /*#__PURE__*/React.createElement("h3", null, "6")), /*#__PURE__*/React.createElement("div", {
    className: "lg-bot"
  }, /*#__PURE__*/React.createElement("div", {
    className: "two-print-rows"
  }, /*#__PURE__*/React.createElement("div", {
    className: "first tr slide"
  }, "Info"), /*#__PURE__*/React.createElement("div", {
    className: "tr slide"
  }, /*#__PURE__*/React.createElement("span", {
    className: "itals"
  }, "Date "), "Picture")))));
}
React.render( /*#__PURE__*/React.createElement(App, null), document.querySelector("#app"));