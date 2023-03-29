import {
  Avatar,
  Box,
  Container,
  Link,
  makeStyles,
  Typography,
} from "@material-ui/core";
import { LockOutlined } from "@material-ui/icons";
import React from "react";

const useStyles = makeStyles((theme) => ({
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
}));

export default function LoginScreen({
  supportEmail,
}: {
  supportEmail: string;
}) {
  const classes = useStyles();

  return (
    <Container component="main" maxWidth="xs">
      <Box
        marginTop={10}
        display="flex"
        flexDirection="column"
        alignItems="center"
      >
        <Avatar className={classes.avatar}>
          <LockOutlined />
        </Avatar>
        <Typography component="h1" variant="h5">
          Login
        </Typography>
        <Box marginY={3}>
          <Typography component="p" variant="body1">
            Login using your e-mail and password.
          </Typography>
        </Box>
      </Box>
      <Typography variant="body2" color="textSecondary" align="center">
        {"Für Hilfe oder weitere Informationen kontaktieren Sie bitte "}
        <Link color="inherit" href={`mailto:${supportEmail}`}>
          {supportEmail}
        </Link>
      </Typography>
    </Container>
  );
}
