# OpenSAFELY ehrQL workshop

This is a template repository for an ehrQL workshop. The tasks are GitHub issues and use two examples: asthma and the QOF diabetes register.

Before the workshop, please work through the [OpenSAFELY getting started guide](https://docs.opensafely.org/getting-started/) and the [ehrQL tutorial](https://docs.opensafely.org/ehrql/tutorials/introduction-to-ehrql/). This workshop builds on those and helps you practise good habits for writing ehrQL and doing reproducible research. You'll:

- Write dataset definitions and measures definitions for realistic examples.
- Work through tasks using GitHub issues.
- Plot your results in R or Python.
- Test your dataset definitions.

Running the workshop? See the [instructor guide](INSTRUCTORS.md).

## Cloning the template repository

1. Click this link to start: https://github.com/bennettoxford/ehrql-demo/generate.
1. Leave the "**Include all branches**" option unchecked
1. In the _General_ section, select your GitHub account as the "**Owner**" and enter a "**Repository name**" and "**Description**"
1. In the _Configuration_ section choose "**Public**" as the repository visibility.
1. Finally, click the "**Create repository**" button.
1. GitHub needs a moment to set up your new repository and create the tasks. **Wait about 1 minute, then reload the page.**

## Setting up a codespace

Create a [GitHub codespace](https://docs.opensafely.org/getting-started/tutorial/create-a-github-codespace/) for your new repository. See also [How to use GitHub Codespaces in your project](https://docs.opensafely.org/getting-started/how-to/use-github-codespaces-in-your-project/).

## Completing the tasks

Your new repository comes with the tasks as GitHub issues. Pick the asthma (`ast`) example, the diabetes (`dm`) example, or both. The task numbers suggest an order, but you can skip around. Tasks 3 and 4 work with any dataset or measures definition.

| Task | Asthma | Diabetes |
| --- | --- | --- |
| Create a dataset definition | Task 1a | Task 1b |
| Calculate monthly prevalence | Task 2a | Task 2b |
| Add ethnicity | Task 3 | Task 3 |
| Add IMD | Task 4 | Task 4 |
| Visualise your results | Task 5 | Task 5 |
| Write assurance tests | Task 6 | Task 6 |

If you're comfortable with Git and GitHub, we recommend creating a new branch for each task and merging it into `main` with a pull request when you're done. This is optional. You can also work directly on `main`.

Each issue tells you which file to work in. If you get stuck, the `solutions/` folder has a solution for Tasks 1, 2, 5 and 6. The files ending in `_dep` contain a depression example.

## Dummy data

In OpenSAFELY you never see real patient data. While you write your code, ehrQL makes up [dummy data](https://docs.opensafely.org/ehrql/how-to/dummy-data/#let-ehrql-generate-a-dummy-dataset-from-your-dataset-definition) based on your dataset or measures definition.

## Resources

- [OpenSAFELY Documentation](https://docs.opensafely.org/)
- [ehrQL Documentation](https://docs.opensafely.org/ehrql/)
- [OpenCodelists](https://www.opencodelists.org/)
- [OpenCodeCounts](https://www.opencodecounts.net/)
- [OpenSAFELY Platform](https://www.opensafely.org/)
- [The OpenSAFELY Demo Repo](https://github.com/bennettoxford/os_training_demonstration)
- [Bennett Institute introductory coding task: Implementing QOF registers in ehrQL](https://github.com/bennettoxford/bennett-research-onboarding-qof)

## Licence

This repository is licensed under the MIT licence, see [`LICENSE`](LICENSE).
