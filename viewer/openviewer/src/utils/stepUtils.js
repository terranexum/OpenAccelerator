const getCurrentStep = (stepStr, stepArray) => {
    const reduceSteps = (foundStep, curStep) => {
        if (curStep.type == "single") {
            return curStep.id == stepStr ? curStep : foundStep;
        } else if (curStep.type == "group") {
            return curStep.steps.reduce(reduceSteps, foundStep);
        }
    }
    return stepArray.reduce(reduceSteps, null);
}

module.exports = {
    getCurrentStep
}