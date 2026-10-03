import ITR1Filing from "./ITR1Filing";
import ITRPlaceholder from "./ITRPlaceholder";
import registryData from "./formRegistry.json";

// Form registry metadata
export const formRegistry = registryData;

// Maps componentName strings in the registry to actual React Component references
export const componentMap = {
  ITR1Filing: ITR1Filing,
  ITR2Placeholder: (props) => <ITRPlaceholder formName="ITR-2" {...props} />,
  ITR3Placeholder: (props) => <ITRPlaceholder formName="ITR-3" {...props} />,
  ITR4Placeholder: (props) => <ITRPlaceholder formName="ITR-4" {...props} />,
};
