import { createFileRoute } from "@tanstack/react-router";
import Prediction from "../components/Common/Prediction";

export const Route = createFileRoute("/prediction")({
  component: Prediction,
});
