//
//
// import React from "react";

import Input from "../../../ui/input";
import Field from "../../../ui/field";

import "./styles.css";

function SumTask({ register, index, type }) {
  return (
    <>
      <Field label="Максимум">
        <Input type="number" {...register(`tasks.${index}.${type}:min`)} />
      </Field>
      <Field label="Минимум">
        <Input type="number" {...register(`tasks.${index}.${type}:max`)} />
      </Field>
      <Field label="Количество слагаемых">
        <Input type="number" {...register(`tasks.${index}.${type}:amount`)} />
      </Field>
    </>
  );
}
// шьзщке шьзщке
// БЮ
export default SumTask;
