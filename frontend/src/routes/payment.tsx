import { createFileRoute } from "@tanstack/react-router";
import Payment from "../components/Common/Payment";

export const Route = createFileRoute("/payment")({
  component: Payment,
});
