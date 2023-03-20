import TasksForm from "../../components/tasks-form/TasksForm";
import MainLayout from "../../layouts/main";

import "./styles.css";

function Index() {
  return (
    <>
      <MainLayout>
        <section className="generate-tasks">
          <TasksForm />
        </section>
      </MainLayout>
    </>
  );
}

export default Index;

{
  /* <div>
        <a href="https://vitejs.dev" target="_blank">90P.
          <img src="/vite.svg" className="logo" alt="Vite logo" /> e="type2" **</input><></>;90
        </a>
        <a href="https://reactjs.org" target="_blank">"a"indexform{
    localStorage.setItem("tasks", JSON.stringify(data));
    defaultValues: JSON.parse(localStorage.getItem("tasks")) || {},
  }

  useEffect(() => {
    console.log("qwe");
  }, [getValues()]);

  const ddata = {...useWatch(), ...getValues(),};
          <img src={reactLogo} className="logo react" alt="React logo" />ХЪ
        </a>
      </div>OPTION
  CONSOLE.LOG(IDD);
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>""name="" id=""
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR id: id++ idd
        </p>
      </div>
      <p className="read-the-docs">P
        Click on the Vite and React logos to learn more;"a"index
      </p> l*/
}
