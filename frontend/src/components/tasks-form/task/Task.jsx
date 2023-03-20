// import React from "react";
import { TaskType, TaskTitle } from "../../../types/task";

import Button from "../../ui/button";
import SumTask from "./sum-task";

import "./styles.css";

function Task({ index, remove, register, id, item, watch }) {
  const type = watch(`tasks.${index}.type`);
  return (
    <div className="task-form__item task">
      <div className="task__header">
        <select {...register(`tasks.${index}.type`)}>
          <option value="" selected disabled hidden>
            Выберите тип задания
          </option>
          {Object.keys(TaskType).map((taskType) => (
            <option value={taskType} className="value" key={taskType}>
              {TaskTitle[taskType]}
            </option>
          ))}
        </select>
        <Button className="task__delete" onClick={() => remove(index)}>
          &#10006;
        </Button>
      </div>
      <div className="task__content">
        {type === TaskType.sum && (
          // <input {...register(`tasks.${index}.${type}:text`)} />X
          <SumTask register={register} index={index} type={type} />
        )}
        {type === "type2" && (
          <input
            type="checkbox"
            {...register(`tasks.${index}.${type}:checked`)}
          />
        )}
        {type === "type3" && (
          <input type="color" {...register(`tasks.${index}.${type}:color`)} />
        )}
      </div>
    </div>
  );
}
// dd
export default Task;
