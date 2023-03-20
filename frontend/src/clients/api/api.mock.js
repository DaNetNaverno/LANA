const getTasks = () => {
  return {
    tasks: [
      { type: "sum" },
      { type: "integral" },
      {
        type: "derivative",
        options: [{ type: "single_number", name: "max_degree" }],
      },
    ],
  };
};

const getVariants = () => {
  return new Promise((res) => {
    setTimeout(res, 1000);
  });
};

export default { getTasksOptions, getVariants };
