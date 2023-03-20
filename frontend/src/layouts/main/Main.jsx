import Header from "../../components/header";
import Footer from "../../components/footer";
import Container from "../../components/container";

import "./style.css";

const Main = ({ children }) => {
  return (
    <div className="app-wrapper">
      <Header />
      <main className="main">
        <Container>{children}</Container>
      </main>
      <Footer />
    </div>
  );
};

export default Main;
