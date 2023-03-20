import { useForm, useFieldArray } from "react-hook-form";

import Task from "./task";
import Input from "../ui/input";
import Button from "../ui/button";
import "./styles.css";

const TasksForm = () => {
  const { handleSubmit, control, register, watch } = useForm({
    defaultValues: {
      "variants-amount": 1,
    },
  });

  const { fields, append, remove } = useFieldArray({ control, name: "tasks" });

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <div className="tasks-form">
      <form
        className="tasks-form form"
        action=""
        onSubmit={handleSubmit(onSubmit)}
      >
        <div className="tasks-form__header">
          <div>
            <label htmlFor="variants-amount" style={{ marginRight: "15px" }}>
              Количество вариантов
            </label>
            <Input
              {...register("variants-amount")}
              width="77px"
              type="number"
              min="1"
              max="100"
            />
          </div>
          <Button onClick={() => append({})} className="tasks-form__button">
            Добавить задание
          </Button>
        </div>
        <div className="task-form__content">
          {fields.map((item, index) => {
            return (
              <Task
                key={item.id}
                id={item.id}
                index={index}
                remove={remove}
                register={register}
                item={item}
                watch={watch}
              />
            );
          })}
        </div>
        <button type="submit">Отправить!</button>
      </form>
    </div>
  );
};

export default TasksForm;
